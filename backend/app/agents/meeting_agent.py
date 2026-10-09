import asyncio
import logging
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright

from backend.app.config.settings import settings
from backend.app.constants.meeting_states import MeetingState
from backend.app.events.meeting_events import (
    MeetingStarted, MeetingJoined, MeetingDisconnected,
    MeetingEnded, BrowserClosed, MeetingFailed
)
from backend.app.core.event_dispatcher import dispatcher

logger = logging.getLogger("ai_lecture_assistant.meeting_agent")

class MeetingAgent:
    """
    Agent responsible for managing the Google Meet lifecycle.
    Handles browser automation using Playwright.
    """
    def __init__(self):
        self.state = MeetingState.IDLE
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.current_meeting_id: Optional[str] = None

    async def _set_state(self, new_state: MeetingState):
        """
        Updates the agent state and logs the transition.
        """
        if self.state != new_state:
            logger.info(f"MeetingAgent State Transition: {self.state.value} -> {new_state.value}")
            self.state = new_state

    async def join_meeting(self, meeting_id: str, url: str):
        """
        Main entry point to join a Google Meet session.
        """
        self.current_meeting_id = meeting_id
        try:
            await self._set_state(MeetingState.STARTING)
            await dispatcher.publish(MeetingStarted(meeting_id=meeting_id, url=url))

            await self._set_state(MeetingState.OPENING_BROWSER)
            await self._launch_browser()

            await self._set_state(MeetingState.JOINING)
            await self._perform_join(url)

            await self._set_state(MeetingState.CONNECTED)
            await dispatcher.publish(MeetingJoined(meeting_id=meeting_id))

            # Start monitoring loop in background
            asyncio.create_task(self._monitor_meeting())

        except Exception as e:
            logger.error(f"Failed to join meeting {meeting_id}: {e}", exc_info=True)
            await self._set_state(MeetingState.ERROR)
            await dispatcher.publish(MeetingFailed(meeting_id=meeting_id, error_message=str(e)))
            await self.leave_meeting()

    async def _launch_browser(self):
        """
        Launches Chromium with a persistent user profile.
        """
        self.playwright = await async_playwright().start()

        # Use launch_persistent_context to reuse login sessions
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=settings.browser.user_data_dir,
            executable_path=settings.browser.executable_path,
            headless=settings.browser.headless,
            args=["--use-fake-ui-for-media-stream"] # Bypass mic/cam permissions
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        logger.info("Browser launched with persistent profile.")

    async def _perform_join(self, url: str):
        """
        Navigates to the Meet URL and interacts with the Join button.
        """
        await self.page.goto(url, timeout=settings.browser.join_timeout)

        # Wait for the 'Join' or 'Ask to join' button
        # Note: Selectors may change; using a general text search for MVP
        try:
            join_button = await self.page.get_by_role("button", name="Join now").or_(
                self.page.get_by_role("button", name="Ask to join")
            ).first

            await join_button.wait_for(state="visible", timeout=10000)
            await join_button.click()

            # Verify successful entry by looking for the 'Leave call' button
            await self.page.get_by_role("button", name="Leave call").wait_for(
                state="visible", timeout=20000
            )
            logger.info("Successfully joined the meeting.")
        except Exception as e:
            logger.error(f"Could not find join button or verify entry: {e}")
            raise RuntimeError("Meeting join failed: Join button not found or entry not verified.")

    async def _monitor_meeting(self):
        """
        Continuously monitors the meeting state.
        """
        logger.info("Meeting monitoring loop started.")
        try:
            while self.state == MeetingState.CONNECTED:
                # Check if the 'Leave call' button is still present
                # If it disappears, the meeting has likely ended or we were removed
                is_present = await self.page.get_by_role("button", name="Leave call").is_visible()

                if not is_present:
                    logger.warning("Meeting end detected (Leave button disappeared).")
                    await self._set_state(MeetingState.DISCONNECTED)
                    await dispatcher.publish(MeetingEnded(meeting_id=self.current_meeting_id))
                    break

                await asyncio.sleep(5) # Poll every 5 seconds
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
            await self._set_state(MeetingState.ERROR)
        finally:
            if self.state == MeetingState.DISCONNECTED:
                await self.leave_meeting()

    async def leave_meeting(self):
        """
        Leaves the meeting and shuts down the browser.
        """
        try:
            if self.page:
                # Try to click 'Leave call' if visible
                leave_btn = self.page.get_by_role("button", name="Leave call")
                if await leave_btn.is_visible():
                    await leave_btn.click()

            await self._set_state(MeetingState.STOPPED)
            logger.info("Left the meeting.")
        except Exception as e:
            logger.warning(f"Error while leaving meeting: {e}")
        finally:
            await self._shutdown_browser()

    async def _shutdown_browser(self):
        """
        Closes browser and playwright resources.
        """
        try:
            if self.context:
                await self.context.close()
            if self.playwright:
                await self.playwright.stop()

            await self._set_state(MeetingState.IDLE)
            await dispatcher.publish(BrowserClosed(meeting_id=self.current_meeting_id))
            logger.info("Browser shut down cleanly.")
        except Exception as e:
            logger.error(f"Error shutting down browser: {e}")

# Singleton instance of the MeetingAgent
meeting_agent = MeetingAgent()

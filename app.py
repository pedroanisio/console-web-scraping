# File: app.py
from config import Config
from services.ChromeRemote import ChromeRemote
from services.Browser import Browser
from model.OreillySite import OreillySite
from services.session.SessionManager import SessionManager
from services.utils.FileLogger import FileLogger

# Initialize logger
logger = FileLogger(log_file=Config.LOG_FILE, log_level=Config.LOG_LEVEL)
if __name__ == "__main__":

    # Log the start of the application
    logger.log_info("Application started.")

    browser = None;
    chrome = None;
    session_manager = None;

    try:
        # Set up ChromeRemote with specified options
        logger.log_debug("Initializing ChromeRemote.")
        chrome = ChromeRemote(logger=logger, options=Config.BROWSER_OPTIONS)

        ## If there no need to store cookies for future sessions, then we can pass None
        logger.log_debug("Initializing SessionManager.")
        session_manager = SessionManager(logger=logger)

        logger.log_debug("Initializing Browser.")        
        browser = Browser(engine=chrome,logger=logger, session_manager=session_manager)

        # Initialize the OreillySite model
        site_config = Config.SITES["oreilly"]
        oreilly_site = OreillySite(browser=browser, logger=logger, config=site_config)
        
        # Check if the user is authenticated
        if oreilly_site.check_authentication():
            logger.log_info("Session is already authenticated.")
        else:
            logger.log_info("Dif not found any auth. Authenticating the session.")
            oreilly_site.authenticate(site_config['credentials'])
     
    except Exception as e:
        logger.log_error(f"An error occurred: {e}")

    finally:
        browser.close()   
        logger.log_info("Application stopped.")
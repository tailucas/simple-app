package simple.app;

import java.io.File;
import java.io.IOException;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.ini4j.Ini;

public class App 
{
    private static Logger log = LoggerFactory.getLogger(App.class);

    private static void registerShutdownHook() {
        final Thread mainThread = Thread.currentThread();
        Runtime.getRuntime().addShutdownHook(new Thread("shutdown hook") {
            public void run() {
                try {
                    log.info("triggered");
                    mainThread.join();
                } catch (InterruptedException ex) {
                    log.error(ex.getMessage(), ex);
                }
            }
        });
    }

    public static void main( String[] args )
    {
        final Locale locale = Locale.getDefault();
        log.info("Locale language: {} ", locale.getLanguage());
        log.info("Locale country: {}", locale.getCountry());
        Thread.currentThread().setName("main");
        registerShutdownHook();
        final Map<String, String> envVars = System.getenv();
        log.info("Starting application with env {}", envVars.keySet());

        final String javaVersion = Runtime.version().toString();
        log.info( "Hello (print) " + javaVersion );
        log.trace("Hello (trace) {} ", javaVersion);
        log.debug("Hello (debug) {} ", javaVersion);
        log.info("Hello (info) {} ", javaVersion);
        log.error("Hello? (error) {}", javaVersion);
        Set<Thread> threadSet = Thread.getAllStackTraces().keySet();
        for (Thread thread : threadSet) {
            log.info(thread + " daemon? " + thread.isDaemon());
        }
        log.info("Working directory is: " + System.getProperty("user.dir"));
        try {
            Ini appConfig = new Ini(new File("config/app.conf"));
            log.info("App Device Name: " + appConfig.get("app", "device_name"));
        } catch (IOException e) {
            log.error(e.getMessage(), e);
        }

        try {
            Thread.currentThread().sleep(2000);
        } catch (InterruptedException e) {
            log.error(e.getMessage(), e);
        }
    }
}

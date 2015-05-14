package fedchenko.igor.samplenotificationapp;

import android.app.Application;

import com.parse.Parse;
import com.parse.ParseInstallation;

public class ApplicationManager extends Application {
    private static ApplicationManager singleton;
    // Возвращает экземпляр данного класса
    public static ApplicationManager getInstance() {
        return singleton;
    }
    @Override
    public final void onCreate() {
        super.onCreate();
        singleton = this;

        Parse.initialize(this, "DUMkDMglUrCy4hmjQtMbMwGN9bwhM5avgW9FQOgW", "k2SihBOM0KH9iGBknFXDX19x9kXaiKjjoGACymiq");

        ParseInstallation.getCurrentInstallation().put("appID", "2");
        ParseInstallation.getCurrentInstallation().saveInBackground();
    }
}

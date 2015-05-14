package fedchenko.igor.samplenotificationapp;

import android.content.Context;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;

/**
 * Created by igor on 05.01.15.
 */
public class NotificationDataManager {

    private static Context AppContext = null;

    private static String StorageFileName = "NotificationsData";
    private static JSONArray NotificationsArray = null;

    /*Singletone*/
    private static NotificationDataManager instance = null;

    public static NotificationDataManager Instance(){
        if (instance == null) instance = new NotificationDataManager();
        return instance;
    }
    /***********/

    public static void SetContext (Context context){
        AppContext = context;
    }

    private NotificationDataManager(){
        File file = new File(AppContext.getFilesDir(), StorageFileName);

        if (!file.exists()) {
            try {
                FileWriter writer = new FileWriter(file);
                writer.write("{\"notifications\":[]}");
                writer.close();
            }
            catch (Exception ex) { ex.printStackTrace();}
        }

        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            StringBuilder sb = new StringBuilder();

            String line = null;
            while ((line = reader.readLine()) != null)
                sb.append(line);
            reader.close();

            JSONObject data = new JSONObject(sb.toString());
            NotificationsArray = data.getJSONArray("notifications");
        }
        catch (Exception ex){ ex.printStackTrace(); }
    }

    public void AddNotificationData(String jsonData)
    {
        try {
            JSONObject notificationObject = new JSONObject(jsonData);
            NotificationsArray.put(notificationObject);
            SaveAllData();
        }
        catch (Exception ex){
            ex.printStackTrace();
        }
    }

    private void SaveAllData(){
        try {
            JSONObject Data = new JSONObject();
            Data.put("notifications", NotificationsArray);
            File file = new File(AppContext.getFilesDir(), StorageFileName);
            FileWriter writer = new FileWriter(file);
            writer.write(Data.toString());
            writer.close();
        }
        catch (Exception ex) { ex.printStackTrace(); }
    }

    public ArrayList<String> GetNotificationsList(){
        ArrayList<String> titles = new ArrayList<>();
        for (int i = 0; i < NotificationsArray.length(); ++i){
            try {
                titles.add(NotificationsArray.getJSONObject(i).getString("alert"));
            }
            catch (Exception ex) { ex.printStackTrace(); }
        }
        return titles;
    }

    public ArrayList<String> GetNewNotifications(ArrayList<String> OldList){
        ArrayList<String> titles = new ArrayList<>();
        for (int i = 0; i < NotificationsArray.length(); ++i){
            try {
                String title = NotificationsArray.getJSONObject(i).getString("alert");
                if (!OldList.contains(title)) titles.add(title);
            }
            catch (Exception ex) { ex.printStackTrace(); }
        }
        return titles;
    }

}

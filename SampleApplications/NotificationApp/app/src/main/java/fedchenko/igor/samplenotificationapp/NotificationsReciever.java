package fedchenko.igor.samplenotificationapp;

import android.app.Activity;
import android.app.TaskStackBuilder;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.util.Log;

import com.parse.ParseAnalytics;
import com.parse.ParsePushBroadcastReceiver;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by igor on 05.01.15.
 */
public class NotificationsReciever extends ParsePushBroadcastReceiver {

    @Override
    protected void onPushReceive(Context context, Intent intent){
        String data = intent.getStringExtra("com.parse.Data");
        NotificationDataManager.Instance().AddNotificationData(data);
        MainActivity.UpdateNotificationsList();

        super.onPushReceive(context, intent);
    }

    @Override
    public void onPushOpen(Context context, Intent intent) {

        ParseAnalytics.trackAppOpenedInBackground(intent);

        String uriString = null;
        try {
            JSONObject pushData = new JSONObject(intent.getStringExtra("com.parse.Data"));
            uriString = pushData.optString("uri");
        } catch (JSONException e) {
            Log.v("com.parse.ParsePushReceiver", "Unexpected JSONException when receiving push data: ", e);
        }

        Intent activityIntent;
        if (uriString != null && uriString.length() != 0) {
            activityIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(uriString));
        } else {
            activityIntent = new Intent(context, MainActivity.class);
        }
        activityIntent.putExtras(intent.getExtras());
        activityIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        //activityIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        context.startActivity(activityIntent);
    }

}

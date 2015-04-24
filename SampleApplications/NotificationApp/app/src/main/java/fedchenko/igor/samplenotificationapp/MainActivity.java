package fedchenko.igor.samplenotificationapp;

import android.app.Activity;
import android.app.Notification;
import android.os.Bundle;
import android.os.Handler;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.parse.ParseAnalytics;
import com.parse.ParsePush;

import java.util.ArrayList;

public class MainActivity extends Activity {

    static ArrayList<String> NotificationsList = null;
    static ArrayAdapter<String> NotificationsListAdapter = null;

    private ImageView splashImageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ShowLogoScreen(3);
    }

    public void InitMainView(){
        setContentView(R.layout.activity_main);

        NotificationDataManager.SetContext(this);

        NotificationsList = NotificationDataManager.Instance().GetNotificationsList();
        NotificationsListAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_list_item_1, NotificationsList);
        ListView NotificationsListView = (ListView) findViewById(R.id.NotificationListView);
        NotificationsListView.setAdapter(NotificationsListAdapter);
        NotificationsListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                TextView item = (TextView) view;
                ShowToast(item.getText().toString());
            }
        });
    }

    public static void UpdateNotificationsList(){
        ArrayList<String> NewNotifications = NotificationDataManager.Instance().GetNewNotifications(NotificationsList);
        for (String notification : NewNotifications)
            NotificationsListAdapter.add(notification);
        NotificationsListAdapter.notifyDataSetChanged();
    }

    private void ShowToast(String text){
        Toast.makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
    }

    private void ShowLogoScreen(int seconds){
        splashImageView = new ImageView(this);
        splashImageView.setScaleType(ImageView.ScaleType.FIT_XY);
        splashImageView.setImageResource(R.drawable.launch_image);
        setContentView(splashImageView);
        Handler h = new Handler();
        h.postDelayed(new Runnable() {
            public void run() {
                InitMainView();
            }

        }, seconds * 1000);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}

package org.test;    

import java.util.Date;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.telephony.TelephonyManager;
import android.app.Activity;
import android.app.ActivityManager;
import android.os.Bundle;
import java.io.OutputStreamWriter;
import java.io.IOException;
import java.io.File;
import android.util.Log ;
import android.os.Build;

public class Phone extends Activity{
    private Context context = null;
    public static Phone mActivity = null;

    //@Override
        //protested void onStart(){}
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //Hardware.context = this;
        //Action.context = this;
        this.mActivity = this;
        context = this;
    }

    public void acceptCall() {
        if (Build.VERSION.SDK_INT >= 21) {
            Intent answerCalintent = new Intent(context, AcceptCallActivity.class);
            answerCalintent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS);
            answerCalintent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(answerCalintent);
        } else {
            Intent intent = new Intent(context, AcceptCallActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(intent);
        }
    }
}


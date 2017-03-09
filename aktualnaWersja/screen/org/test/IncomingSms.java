package org.test;

import android.content.BroadcastReceiver;
import android.telephony.SmsManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log ;
import java.lang.Object;
import android.telephony.SmsMessage;
import android.speech.tts.TextToSpeech;
import java.util.Locale;

public class IncomingSms extends BroadcastReceiver {

    TextToSpeech t1;
    // Get the object of SmsManager
    final SmsManager sms = SmsManager.getDefault();

    public void onReceive(Context context, Intent intent) {

        t1=new TextToSpeech(context, new TextToSpeech.OnInitListener() {
         @Override
         public void onInit(int status) {
            if(status != TextToSpeech.ERROR) {
               t1.setLanguage(Locale.UK);
            }
         }
      });
        // Retrieves a map of extended data from the intent.
        final Bundle bundle = intent.getExtras();

        System.out.println("dzialasms");
        try {
            String message = "";
            if (bundle != null) {

                final Object[] pdusObj = (Object[]) bundle.get("pdus");

                for (int i = 0; i < pdusObj.length; i++) {

                    SmsMessage currentMessage = SmsMessage.createFromPdu((byte[]) pdusObj[i]);
                    String phoneNumber = currentMessage.getDisplayOriginatingAddress();

                    String senderNum = phoneNumber;
                    message = currentMessage.getDisplayMessageBody();
                    //textSMS = message;
                    //telSMS = senderNum;

                    Log.i("SmsReceiver", "senderNum_test: "+ senderNum + "; message_test: " + message);
                    // Show Alert
                    //int duration = Toast.LENGTH_LONG;
                    //Toast toast = Toast.makeText(context,
                                 //"senderNum_test: "+ senderNum + ", message_test: " + message, duration);
                    //toast.show();


                } // end for loop
              } // bundle is null






            t1.speak(message, TextToSpeech.QUEUE_FLUSH, null);
            //t1.stop();
            //t1.shutdown();


        } catch (Exception e) {
            Log.e("SmsReceiver", "Exception smsReceiver" +e);

        }
    }
}

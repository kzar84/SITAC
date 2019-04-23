package com.example.sitac;

import java.io.*;
import java.net.*;
import java.lang.String;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    public static String alarm_time_hour = "2";
    public static String alarm_time_minute = "02";
    public static String alarm_time_a_or_p = "AM";
    public static String alarm_set = "true";
    public static String brew_time_hour = "3";
    public static String brew_time_minute = "47";
    public static String brew_time_a_or_p = "PM";
    public static String brew_set = "false";
    public static String lights_set = "false";
    public static String alarm_tone = "Buzzer";
    public static String volume = "8";

    Button welcomeButton;
    String address = "172.20.10.7";
    int port = 8080;
    byte[] messageByte = new byte[1];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        welcomeButton = findViewById(R.id.button);
        welcomeButton.setOnClickListener(new OnClickListener(){
            @Override
            public void onClick(View view) {
                try {
                    tryConnecting();
                    goToSettings(view);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void goToSettings(View view){
        Intent intent = new Intent(this, Settings.class);
        startActivity(intent);
    }

    public void useParser(String response){
        String[] defaults = response.split(",");
        alarm_time_hour = defaults[0];
        alarm_time_minute = defaults[1];
        alarm_time_a_or_p = defaults[2];
        alarm_set = defaults[3];
        brew_time_hour = defaults[4];
        brew_time_minute = defaults[5];
        brew_time_a_or_p = defaults[6];
        brew_set = defaults[7];
        lights_set = defaults[8];
        alarm_tone = defaults[9];
        volume = defaults[10];
    }

    public void tryConnecting() throws InterruptedException {
        Thread t = new Thread(new Runnable() {
            public void run(){
                Log.d("Test2", "we got to here");
                try {
                    String message = "send";
                    Log.d("Test", "we got to here");
                    Socket socket = new Socket(address,port);
                    OutputStream out = socket.getOutputStream();
                    byte[] output_message = message.getBytes();
                    out.write(output_message,0,output_message.length);
                    Log.d("Test3b", "we got to here");
                    Log.d("Test5", "we got to here");
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    //InputStream in = socket.getInputStream();
                    Log.d("Test6", "we got to here");
                    String readValues = "";
                    String response = "";
                    while((readValues = in.readLine()) != null) {
                        response += readValues;
                        Log.d("Tester", "we got to here");
                    }
                    Log.d("Test7", response);
                    useParser(response);
                    Log.d("Test8", "we got to here");
                    in.close();
                    out.close();
                    Log.d("Test9", "we got to here");
                    socket.close();
                    Log.d("Test10", "we got to here");
                } catch (UnknownHostException e) {
                    Log.d("Test3", "we got to here");
                    e.printStackTrace();
                } catch (IOException e) {
                    Log.d("Test4", "we got to here");
                    e.printStackTrace();
                }
            }
        });
        t.start();
        t.join();
    }
}

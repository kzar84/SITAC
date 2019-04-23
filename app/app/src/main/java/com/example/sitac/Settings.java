package com.example.sitac;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.Switch;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

import static com.example.sitac.MainActivity.alarm_time_hour;
import static com.example.sitac.MainActivity.alarm_time_minute;
import static com.example.sitac.MainActivity.alarm_time_a_or_p;
import static com.example.sitac.MainActivity.alarm_set;
import static com.example.sitac.MainActivity.brew_time_hour;
import static com.example.sitac.MainActivity.brew_time_minute;
import static com.example.sitac.MainActivity.brew_time_a_or_p;
import static com.example.sitac.MainActivity.brew_set;
import static com.example.sitac.MainActivity.lights_set;
import static com.example.sitac.MainActivity.alarm_tone;
import static com.example.sitac.MainActivity.volume;

public class Settings extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        Spinner dropdown1 = findViewById(R.id.spinner);
        String[] items1 = new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"};
        ArrayAdapter<String> adapter1 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items1);
        dropdown1.setAdapter(adapter1);
        dropdown1.setSelection(Integer.parseInt(alarm_time_hour)-1);

        Spinner dropdown2 = findViewById(R.id.spinner2);
        String[] items2 = new String[]{"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
        "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28",
        "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44",
        "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"};
        ArrayAdapter<String> adapter2 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items2);
        dropdown2.setAdapter(adapter2);
        dropdown2.setSelection(Integer.parseInt(alarm_time_minute));

        Spinner dropdown3 = findViewById(R.id.spinner3);
        String[] items3 = new String[]{"AM", "PM"};
        ArrayAdapter<String> adapter3 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items3);
        dropdown3.setAdapter(adapter3);
        int selection_num3;
        if(alarm_time_a_or_p.equals("AM")){
            selection_num3 = 0;
        }else{
            selection_num3 = 1;
        }
        dropdown3.setSelection(selection_num3);

        Spinner dropdown4 = findViewById(R.id.spinner4);
        String[] items4 = new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"};
        ArrayAdapter<String> adapter4 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items4);
        dropdown4.setAdapter(adapter4);
        dropdown4.setSelection(Integer.parseInt(brew_time_hour)-1);

        Spinner dropdown5 = findViewById(R.id.spinner5);
        String[] items5 = new String[]{"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28",
                "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44",
                "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"};
        ArrayAdapter<String> adapter5 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items5);
        dropdown5.setAdapter(adapter5);
        dropdown5.setSelection(Integer.parseInt(brew_time_minute));

        Spinner dropdown6 = findViewById(R.id.spinner6);
        String[] items6 = new String[]{"AM", "PM"};
        ArrayAdapter<String> adapter6 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items6);
        dropdown6.setAdapter(adapter6);
        int selection_num6;
        if(brew_time_a_or_p.equals("AM")){
            selection_num6 = 0;
        }else{
            selection_num6 = 1;
        }
        dropdown6.setSelection(selection_num6);

        Spinner dropdown7 = findViewById(R.id.spinner7);
        String[] items7 = new String[]{"Buzzer", "Police"};
        ArrayAdapter<String> adapter7 = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items7);
        dropdown7.setAdapter(adapter7);
        int selection_num7;
        if(alarm_tone.equals("Buzzer")){
            selection_num7 = 0;
        }else{
            selection_num7 = 1;
        }
        dropdown7.setSelection(selection_num7);

        Switch lightSwitch = findViewById(R.id.switch1);
        lightSwitch.setChecked(Boolean.parseBoolean(lights_set));

        Switch alarmSwitch = findViewById(R.id.switch2);
        alarmSwitch.setChecked(Boolean.parseBoolean(alarm_set));

        Switch brewSwitch = findViewById(R.id.switch3);
        brewSwitch.setChecked(Boolean.parseBoolean(brew_set));

        SeekBar volumeSlider = findViewById(R.id.seekBar);
        volumeSlider.setProgress(Integer.parseInt(volume));

        Button updateButton = findViewById(R.id.button2);
        updateButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                tryConnecting();
                goToMainActivity(view);
            }
        });
    }

    public void goToMainActivity(View view){
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }

    public String messageCreate(){
        String message = "";
        Spinner new_alarm_time_hour = findViewById(R.id.spinner);
        message += new_alarm_time_hour.getSelectedItem().toString();
        message += ",";
        Spinner new_alarm_time_minute = findViewById(R.id.spinner2);
        message += new_alarm_time_minute.getSelectedItem().toString();
        message += ",";
        Spinner new_alarm_time_a_or_p = findViewById(R.id.spinner3);
        message += new_alarm_time_a_or_p.getSelectedItem().toString();
        message += ",";
        Switch new_alarm_set = findViewById(R.id.switch2);
        if(new_alarm_set.isChecked()){
            message += "True,";
        } else {
            message += "False,";
        }
        Spinner new_brew_time_hour = findViewById(R.id.spinner4);
        message += new_brew_time_hour.getSelectedItem().toString();
        message += ",";
        Spinner new_brew_time_minute = findViewById(R.id.spinner5);
        message += new_brew_time_minute.getSelectedItem().toString();
        message += ",";
        Spinner new_brew_time_a_or_p = findViewById(R.id.spinner6);
        message += new_brew_time_a_or_p.getSelectedItem().toString();
        message += ",";
        Switch new_brew_set = findViewById(R.id.switch3);
        if(new_brew_set.isChecked()){
            message += "True,";
        } else {
            message += "False,";
        }
        Switch new_lights_set = findViewById(R.id.switch1);
        if(new_lights_set.isChecked()){
            message += "True,";
        } else {
            message += "False,";
        }
        Spinner new_alarm_tone = findViewById(R.id.spinner7);
        message += new_alarm_tone.getSelectedItem().toString();
        message += ",";
        SeekBar new_volume = findViewById(R.id.seekBar);
        int volume_level = new_volume.getProgress();
        message += Integer.toString(volume_level);
        return message;
    }

    public void tryConnecting(){
        new Thread(new Runnable() {
            public void run(){
                String message = messageCreate();
                try {
                    Log.d("Testb", "we got to here");
                    Socket socket = new Socket("172.20.10.7",8080); //update when we find correct address
                    OutputStream out = socket.getOutputStream();
                    Log.d("Test2b", "we got to here");
                    byte[] output_message = message.getBytes();
                    out.write(output_message,0,output_message.length);
                    Log.d("Test3b", "we got to here");
                    out.close();
                    Log.d("Test4b", "we got to here");
                    socket.close();
                    Log.d("Test5b", "we got to here");
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();

    }

}

package io.github.romerski.rogally;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.tv.TvContract;
import android.media.tv.TvInputInfo;
import android.media.tv.TvInputManager;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Toast;

import java.util.Collections;
import java.util.List;
import java.util.Locale;

/**
 * Home tile for the ASUS ROG Ally on its dock: switches the TV to the Ally's HDMI input and closes.
 *
 * Which input, in this order:
 *  1. one named after the Ally: its HDMI-CEC device name ("ASUS ROG Ally"), or the name given to its port in
 *     Settings > Inputs. Not always there: the dock does not always announce itself over CEC.
 *  2. the only HDMI port with something switched on behind it. TCL reports an empty port as standby, so with the
 *     Ally as the one HDMI device this follows the cable to whatever port it is moved to.
 *  3. the port it was last found on, then HDMI 2, where it was first set up.
 */
public class MainActivity extends Activity {
    /** TCL's Live TV app, which plays the HDMI inputs. */
    private static final String TV_APP = "com.tcl.tv";
    /** HDMI 2 on the TCL 75C89K. */
    private static final String HDMI_2 = "com.tcl.tvinput/.TvPassThroughService/HW16";
    private static final String NAME = "ally";
    private static final String PREFS = "ally", LAST_PORT = "last_port";

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        open(pickInput());
        finish();
        overridePendingTransition(0, 0);
    }

    private String pickInput() {
        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        TvInputManager tim = (TvInputManager) getSystemService(TV_INPUT_SERVICE);
        List<TvInputInfo> inputs = Collections.emptyList();
        if (tim != null) {
            try {
                inputs = tim.getTvInputList();
            } catch (RuntimeException ignored) {
            }
        }
        for (TvInputInfo info : inputs) {
            if (!info.isPassthroughInput()) continue;
            if (named(info.loadLabel(this)) || named(info.loadCustomLabel(this))) {
                String port = info.getParentId() != null ? info.getParentId() : info.getId();
                prefs.edit().putString(LAST_PORT, port).apply();
                return info.getId();
            }
        }
        String only = null;
        int connected = 0;
        for (TvInputInfo info : inputs) {
            if (!info.isPassthroughInput() || info.getType() != TvInputInfo.TYPE_HDMI || info.getParentId() != null) {
                continue;
            }
            if (tim.getInputState(info.getId()) == TvInputManager.INPUT_STATE_CONNECTED) {
                connected++;
                only = info.getId();
            }
        }
        if (connected == 1) {
            prefs.edit().putString(LAST_PORT, only).apply();
            return only;
        }
        return prefs.getString(LAST_PORT, HDMI_2);
    }

    private static boolean named(CharSequence label) {
        return label != null && label.toString().toLowerCase(Locale.ROOT).contains(NAME);
    }

    /** The same channel URI the TV's own source panel and the CleanYourTV Inputs menu send. */
    private void open(String inputId) {
        Uri uri = TvContract.buildChannelUriForPassthroughInput(inputId);
        Intent view = new Intent(Intent.ACTION_VIEW)
                .setDataAndType(uri, "vnd.android.cursor.item/channel")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            startActivity(new Intent(view).setPackage(TV_APP));
            return;
        } catch (ActivityNotFoundException | SecurityException ignored) {
        }
        try {
            startActivity(view);
        } catch (ActivityNotFoundException | SecurityException e) {
            Toast.makeText(this, R.string.not_available, Toast.LENGTH_SHORT).show();
        }
    }
}

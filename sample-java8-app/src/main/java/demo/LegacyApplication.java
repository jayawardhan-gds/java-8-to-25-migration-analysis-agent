package demo;

import java.util.Calendar;
import java.util.Date;
import java.util.Hashtable;

public class LegacyApplication {
    public String summary() {
        Date now = new Date();
        Calendar calendar = Calendar.getInstance();
        Hashtable<String, String> values = new Hashtable<>();
        values.put("date", now.toString());
        return values.get("date") + " year=" + calendar.get(Calendar.YEAR);
    }
}

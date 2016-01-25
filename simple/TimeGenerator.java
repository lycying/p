import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by yaoboxun on 14-7-8.
 */
public class TimeGenerator {

  public static void main(String[] args) {
    if(args.length == 0) {
      return;
    }
    //String beginTime = args[0];
    //String endTime = args[1];
    String beginTime = "09:00:00";
    String endTime = "10:00:00";
    SimpleDateFormat sdf = new SimpleDateFormat("hh:mm:ss");
    Date randomDate = randomDate(beginTime, endTime);
    String randomDates = sdf.format(randomDate);
    System.out.println(randomDates);
  }

  private static Date randomDate(String beginTime, String endTime) {
    try {
      SimpleDateFormat sdf = new SimpleDateFormat("hh:mm:ss");
      Date start = sdf.parse(beginTime);
      Date end = sdf.parse(endTime);

      if(start.getTime() >= end.getTime()) return null;

      long date = random(start.getTime(), end.getTime());
      return new Date(date);
    } catch (Exception e) {
      e.printStackTrace();
    }
    return null;
  }

  private static long random(long begin, long end) {
    long rtn = begin + (long) (Math.random() * (end - begin));
    if(rtn == begin || rtn == end) {
      return random(begin, end);
    }
    return rtn;
  }
}

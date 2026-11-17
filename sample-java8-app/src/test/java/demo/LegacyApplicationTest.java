package demo;
import org.junit.Test;
import static org.junit.Assert.assertTrue;
public class LegacyApplicationTest {
    @Test public void summaryContainsYear() { assertTrue(new LegacyApplication().summary().contains("year=")); }
}

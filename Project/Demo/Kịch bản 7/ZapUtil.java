package ZapUtil;

import org.openqa.selenium.Proxy;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.WebDriver;
import org.zaproxy.clientapi.core.ApiResponse;
import org.zaproxy.clientapi.core.ApiResponseElement;
import org.zaproxy.clientapi.core.ClientApi;
import org.zaproxy.clientapi.core.ClientApiException;

public class ZapUtil {
    private static ClientApi clientApi;
    public static Proxy proxy;

    private static final String zapAddress = "127.0.0.1";
    private static final int zapPort = 8080;
    private static final String apiKey = "ke8gh041f49e3olh5hnqf1k3qt";

    static {
        clientApi = new ClientApi(zapAddress, zapPort, apiKey);
        proxy = new Proxy().setSslProxy(zapAddress + ":" + zapPort).setHttpProxy(zapAddress + ":" + zapPort);
    }

    public static void main(String[] args) {
        String target = "https://ginandjuice.shop/";
        WebDriver driver = null;
        try {
            // Thiết lập proxy cho trình duyệt
            EdgeOptions options = new EdgeOptions();
            options.setProxy(proxy);
            driver = new EdgeDriver(options);

            // Mở trang web mục tiêu
            driver.get(target);

            // Đợi một lúc để đảm bảo rằng tất cả traffic đã được ghi nhận
            Thread.sleep(15000);

            // Bắt đầu quét chủ động
            ApiResponse scanResponse = clientApi.ascan.scan(target, "True", "False", null, null, null);
            String scanId = ((ApiResponseElement) scanResponse).getValue();

            int progress = 0;
            while (progress < 100) {
                progress = Integer.parseInt(((ApiResponseElement) clientApi.ascan.status(scanId)).getValue());
                System.out.println("Scan progress: " + progress + "%");
                Thread.sleep(10000);
            }
            System.out.println("Scan completed");

            // Chờ cho passive scan hoàn tất
            waitTillPassiveScanComplete();

            // Tạo báo cáo
            generateZapReport(target);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (driver != null) {
                driver.quit();
            }
        }
    }

    public static void waitTillPassiveScanComplete() {
        try {
            ApiResponse apiResponse = clientApi.pscan.recordsToScan();
            String tempVal = ((ApiResponseElement) apiResponse).getValue();
            while (!tempVal.equals("0")) {
                System.out.println("Passive scan in progress, remaining records: " + tempVal);
                Thread.sleep(1000);
                apiResponse = clientApi.pscan.recordsToScan();
                tempVal = ((ApiResponseElement) apiResponse).getValue();
            }
            System.out.println("Passive scan completed");
        } catch (ClientApiException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void generateZapReport(String site_to_test) {
        String title = "Demo Title";
        String template = "traditional-html";
        String theme = null;
        String description = "Demo description";
        String contexts = null;
        String sites = site_to_test;
        String sections = null;
        String includedconfidences = null;
        String includedrisks = null;
        String reportfilename = "hihihi";
        String reportfilenamepattern = null;
        String reportdir = System.getProperty("user.dir");
        String display = null;
        try {
            clientApi.reports.generate(title, template, theme, description, contexts, sites, sections,
                    includedconfidences, includedrisks, reportfilename, reportfilenamepattern, reportdir, display);
            System.out.println("Report generation completed successfully.");
        } catch (ClientApiException e) {
            e.printStackTrace();
            System.out.println("Retrying report generation due to connection error...");
            try {
                Thread.sleep(5000);
                clientApi.reports.generate(title, template, theme, description, contexts, sites, sections,
                        includedconfidences, includedrisks, reportfilename, reportfilenamepattern, reportdir, display);
                System.out.println("Report generation completed successfully on retry.");
            } catch (ClientApiException | InterruptedException retryException) {
                retryException.printStackTrace();
            }
        }
    }
}

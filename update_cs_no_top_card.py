import os

cs_file = r"C:\Users\syedw\source\repos\Air Quality\Air Quality\Views\DashboardPage.xaml.cs"

code = """using Air_Quality.Models;
using Air_Quality.Drawables;
using LiveChartsCore;
using LiveChartsCore.SkiaSharpView;
using LiveChartsCore.SkiaSharpView.Painting;
using SkiaSharp;
using System.Collections.ObjectModel;
using System.Net.Http.Json;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Graphics;

namespace Air_Quality.Views;

public partial class DashboardPage : ContentPage
{
    private readonly HttpClient client = new HttpClient();
    private readonly HttpClient aiClient = new HttpClient();

    // AI Prediction API Endpoint (Server goes online @ 9 PM)
    private const string PredictionUrl = "https://bankbook-dastardly-duckbill.ngrok-free.dev/predict";
    private const string FirebaseBase = "https://indoor-air-quality-3251a-default-rtdb.europe-west1.firebasedatabase.app/";
    private const string FirebaseAuth = "aYL4XqOTMYPte3iRCkA3Wy4EDtFeUptUYebLm98D";

    // Gauge Drawables
    private readonly MetricGaugeDrawable co2Drawable = new MetricGaugeDrawable { Unit = "ppm", MaxValue = 2000f, AccentColor = Color.FromArgb("#10B981") };
    private readonly MetricGaugeDrawable pm25Drawable = new MetricGaugeDrawable { Unit = "µg/m³", MaxValue = 100f, AccentColor = Color.FromArgb("#3B82F6") };
    private readonly MetricGaugeDrawable tempDrawable = new MetricGaugeDrawable { Unit = "°C", MaxValue = 50f, AccentColor = Color.FromArgb("#00F2FE") };
    private readonly MetricGaugeDrawable humidityDrawable = new MetricGaugeDrawable { Unit = "%", MaxValue = 100f, AccentColor = Color.FromArgb("#A855F7") };

    // Live Telemetry Collections
    private readonly ObservableCollection<double> temperatureValues = new();
    private readonly ObservableCollection<double> co2Values = new();
    private readonly ObservableCollection<double> pm25Values = new();
    private readonly ObservableCollection<double> tvocValues = new();

    private string currentChartMetric = "Temp";

    public DashboardPage()
    {
        InitializeComponent();
        
        aiClient.DefaultRequestHeaders.Add("ngrok-skip-browser-warning", "true");

        // Assign Drawables to Mini-Gauges
        Co2GaugeView.Drawable = co2Drawable;
        Pm25GaugeView.Drawable = pm25Drawable;
        TempGaugeView.Drawable = tempDrawable;
        HumidityGaugeView.Drawable = humidityDrawable;

        // Initialize Chart Axes
        SensorChart.XAxes = new Axis[]
        {
            new Axis
            {
                TextSize = 11,
                LabelsPaint = new SolidColorPaint(SKColors.SlateGray)
            }
        };

        SensorChart.YAxes = new Axis[]
        {
            new Axis
            {
                TextSize = 11,
                MinStep = 1,
                LabelsPaint = new SolidColorPaint(SKColors.SlateGray)
            }
        };

        SetChartSeries("Temp");
        _ = StartReadingFirebase();
    }

    private void SetChartSeries(string metric)
    {
        currentChartMetric = metric;

        if (metric == "Temp")
        {
            SensorChart.Series = new ISeries[]
            {
                new LineSeries<double>
                {
                    Values = temperatureValues,
                    Name = "Temperature",
                    GeometrySize = 6,
                    LineSmoothness = 0.7,
                    Fill = new SolidColorPaint(SKColor.Parse("#1A00F2FE")),
                    Stroke = new SolidColorPaint(SKColor.Parse("#00F2FE"), 3),
                    GeometryStroke = new SolidColorPaint(SKColors.White, 2),
                    GeometryFill = new SolidColorPaint(SKColor.Parse("#00F2FE"))
                }
            };
        }
        else if (metric == "CO2")
        {
            SensorChart.Series = new ISeries[]
            {
                new LineSeries<double>
                {
                    Values = co2Values,
                    Name = "CO2",
                    GeometrySize = 6,
                    LineSmoothness = 0.7,
                    Fill = new SolidColorPaint(SKColor.Parse("#1A10B981")),
                    Stroke = new SolidColorPaint(SKColor.Parse("#10B981"), 3),
                    GeometryStroke = new SolidColorPaint(SKColors.White, 2),
                    GeometryFill = new SolidColorPaint(SKColor.Parse("#10B981"))
                }
            };
        }
        else if (metric == "PM25")
        {
            SensorChart.Series = new ISeries[]
            {
                new LineSeries<double>
                {
                    Values = pm25Values,
                    Name = "PM2.5",
                    GeometrySize = 6,
                    LineSmoothness = 0.7,
                    Fill = new SolidColorPaint(SKColor.Parse("#1A3B82F6")),
                    Stroke = new SolidColorPaint(SKColor.Parse("#3B82F6"), 3),
                    GeometryStroke = new SolidColorPaint(SKColors.White, 2),
                    GeometryFill = new SolidColorPaint(SKColor.Parse("#3B82F6"))
                }
            };
        }
        else if (metric == "TVOC")
        {
            SensorChart.Series = new ISeries[]
            {
                new LineSeries<double>
                {
                    Values = tvocValues,
                    Name = "TVOC",
                    GeometrySize = 6,
                    LineSmoothness = 0.7,
                    Fill = new SolidColorPaint(SKColor.Parse("#1AF59E0B")),
                    Stroke = new SolidColorPaint(SKColor.Parse("#F59E0B"), 3),
                    GeometryStroke = new SolidColorPaint(SKColors.White, 2),
                    GeometryFill = new SolidColorPaint(SKColor.Parse("#F59E0B"))
                }
            };
        }
    }

    private void OnTempChartClicked(object sender, EventArgs e) => SetChartSeries("Temp");
    private void OnCo2ChartClicked(object sender, EventArgs e) => SetChartSeries("CO2");
    private void OnPm25ChartClicked(object sender, EventArgs e) => SetChartSeries("PM25");
    private void OnTvocChartClicked(object sender, EventArgs e) => SetChartSeries("TVOC");

    private async Task PredictAirQuality(SensorModel sensor)
    {
        try
        {
            var request = new PredictionRequest
            {
                timestamp = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss"),
                device_id = "IAQ_NODE_01",
                SCD41 = new SCD41
                {
                    co2_ppm = sensor.co2,
                    temp_c = sensor.temp,
                    humidity_pct = sensor.rh
                },
                SPS30 = new SPS30
                {
                    pm1_ugm3 = sensor.pm1,
                    pm25_ugm3 = sensor.pm25,
                    pm4_ugm3 = sensor.pm4,
                    pm10_ugm3 = sensor.pm10
                },
                CCS811 = new CCS811
                {
                    eco2_ppm = sensor.eco2,
                    tvoc_ppb = sensor.tvoc
                }
            };

            var response = await aiClient.PostAsJsonAsync(PredictionUrl, request);

            if (!response.IsSuccessStatusCode)
            {
                // When AI Server is offline before 9 PM
                PredictionLabel.Text = "AI MODEL OFFLINE";
                ConfidenceLabel.Text = "Confidence : --%";
                StatusLabel.Text = "Server Going Live @ 9 PM • Waiting for AI Stream";
                return;
            }

            var result = await response.Content.ReadFromJsonAsync<PredictionResponse>();

            if (result != null && result.air_quality != null)
            {
                string label = result.air_quality.label ?? "OPTIMAL";
                double confidence = result.air_quality.confidence;
                string status = result.anomaly?.status ?? "System Normal";

                // Update Labels strictly from AI Model Output
                PredictionLabel.Text = label.ToUpper();
                ConfidenceLabel.Text = $"Confidence : {confidence:F1}%";
                StatusLabel.Text = status;
            }
        }
        catch (Exception)
        {
            PredictionLabel.Text = "AI MODEL OFFLINE";
            ConfidenceLabel.Text = "Confidence : --%";
            StatusLabel.Text = "Server Going Live @ 9 PM • Waiting for AI Stream";
        }
    }

    private async Task LoadSensorData()
    {
        try
        {
            string url = $"{FirebaseBase}/sensor_data.json?auth={FirebaseAuth}";
            var data = await client.GetFromJsonAsync<Dictionary<string, SensorModel>>(url);

            if (data != null && data.Count > 0)
            {
                var latest = data.Last().Value;

                // 1. Update Mini Gauges from Hardware Sensors
                co2Drawable.Value = (float)latest.co2;
                Co2GaugeView.Invalidate();

                pm25Drawable.Value = (float)latest.pm25;
                Pm25GaugeView.Invalidate();

                tempDrawable.Value = (float)latest.temp;
                TempGaugeView.Invalidate();

                humidityDrawable.Value = (float)latest.rh;
                HumidityGaugeView.Invalidate();

                // 2. Update Labels
                TempLabel.Text = $"{latest.temp:F1} °C";
                HumidityLabel.Text = $"{latest.rh:F1} %";
                CO2Label.Text = $"{latest.co2:F0} ppm";
                ECO2Label.Text = $"{latest.eco2:F0} ppm";
                TVOCLabel.Text = $"{latest.tvoc:F0} ppb";

                PM1Label.Text = $"{latest.pm1:F1} µg/m³";
                PM25Label.Text = $"{latest.pm25:F1} µg/m³";
                PM4Label.Text = $"{latest.pm4:F1} µg/m³";
                PM10Label.Text = $"{latest.pm10:F1} µg/m³";

                TimestampLabel.Text = latest.timestamp ?? DateTime.Now.ToString("HH:mm:ss");

                // 3. Update Chart Collections
                temperatureValues.Add(latest.temp);
                co2Values.Add(latest.co2);
                pm25Values.Add(latest.pm25);
                tvocValues.Add(latest.tvoc);

                if (temperatureValues.Count > 20) temperatureValues.RemoveAt(0);
                if (co2Values.Count > 20) co2Values.RemoveAt(0);
                if (pm25Values.Count > 20) pm25Values.RemoveAt(0);
                if (tvocValues.Count > 20) tvocValues.RemoveAt(0);

                // 4. Request AI Model Prediction
                await PredictAirQuality(latest);
            }
        }
        catch (Exception)
        {
        }
    }

    private async void RefreshView_Refreshing(object sender, EventArgs e)
    {
        try
        {
            await LoadSensorData();
        }
        finally
        {
            RefreshView.IsRefreshing = false;
        }
    }

    private async Task StartReadingFirebase()
    {
        while (true)
        {
            await LoadSensorData();
            await Task.Delay(3000);
        }
    }
}
"""

with open(cs_file, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated DashboardPage.xaml.cs removing top AQI gauge card references!")

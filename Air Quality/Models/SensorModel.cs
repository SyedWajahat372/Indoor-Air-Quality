namespace Air_Quality.Models;

public class SensorModel
{
    public double co2 { get; set; }

    public double eco2 { get; set; }

    public double temp { get; set; }

    public double rh { get; set; }

    public double tvoc { get; set; }

    public double pm1 { get; set; }

    public double pm25 { get; set; }

    public double pm4 { get; set; }

    public double pm10 { get; set; }

    public string timestamp { get; set; }
}
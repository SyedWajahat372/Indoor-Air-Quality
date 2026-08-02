using System.Text.Json.Serialization;

namespace Air_Quality.Models;

public class SCD41
{
    [JsonPropertyName("CO2_ppm")]
    public double CO2_ppm { get; set; }

    [JsonPropertyName("Temp_C")]
    public double Temp_C { get; set; }

    [JsonPropertyName("Humidity_pct")]
    public double Humidity_pct { get; set; }
}

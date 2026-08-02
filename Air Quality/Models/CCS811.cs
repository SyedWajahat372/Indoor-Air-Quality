using System.Text.Json.Serialization;

namespace Air_Quality.Models;

public class CCS811
{
    [JsonPropertyName("eCO2_ppm")]
    public double eCO2_ppm { get; set; }

    [JsonPropertyName("TVOC_ppb")]
    public double TVOC_ppb { get; set; }
}

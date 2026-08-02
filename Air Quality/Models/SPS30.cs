using System.Text.Json.Serialization;

namespace Air_Quality.Models;

public class SPS30
{
    [JsonPropertyName("PM25_ugm3")]
    public double PM25_ugm3 { get; set; }
}
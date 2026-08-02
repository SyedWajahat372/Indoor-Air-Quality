using System.Text.Json.Serialization;

namespace Air_Quality.Models;

public class PredictionResponse
{
    public string timestamp { get; set; }
    public string device_id { get; set; }

    [JsonPropertyName("AQ_label")]
    public string AQ_label { get; set; }

    [JsonPropertyName("confidence_pct")]
    public double confidence_pct { get; set; }

    [JsonPropertyName("is_anomaly")]
    public bool is_anomaly { get; set; }

    [JsonPropertyName("anomaly_score")]
    public double anomaly_score { get; set; }

    public string processed_at { get; set; }
}

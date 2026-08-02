using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json.Serialization;


namespace Air_Quality.Models;

public class PredictionRequest
{
    public string timestamp { get; set; }

    public string device_id { get; set; }


    [JsonPropertyName("SCD41")]
    public SCD41 SCD41 { get; set; }


    [JsonPropertyName("SPS30")]
    public SPS30 SPS30 { get; set; }


    [JsonPropertyName("CCS811")]
    public CCS811 CCS811 { get; set; }
}
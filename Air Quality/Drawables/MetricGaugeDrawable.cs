using System;
using Microsoft.Maui.Graphics;

namespace Air_Quality.Drawables;

public class MetricGaugeDrawable : IDrawable
{
    public float Value { get; set; } = 480f;
    public float MaxValue { get; set; } = 2000f;
    public string Unit { get; set; } = "ppm";
    public Color AccentColor { get; set; } = Color.FromArgb("#10B981");

    public void Draw(ICanvas canvas, RectF dirtyRect)
    {
        canvas.Antialias = true;

        float width = dirtyRect.Width;
        float height = dirtyRect.Height;
        float centerX = width / 2f;
        float centerY = height / 2f;
        float radius = Math.Min(centerX, centerY) - 10f;

        float startAngle = 140f;
        float sweepAngle = 260f;

        // Background Track Arc
        canvas.StrokeColor = Color.FromArgb("#1FFFFFFF");
        canvas.StrokeSize = 10f;
        canvas.StrokeLineCap = LineCap.Round;
        canvas.DrawArc(centerX - radius, centerY - radius, radius * 2, radius * 2, startAngle, startAngle + sweepAngle, false, false);

        // Active Arc
        float ratio = Math.Min(1f, Math.Max(0f, Value / MaxValue));
        float currentSweep = sweepAngle * ratio;

        canvas.StrokeColor = AccentColor;
        canvas.StrokeSize = 10f;
        canvas.StrokeLineCap = LineCap.Round;
        canvas.DrawArc(centerX - radius, centerY - radius, radius * 2, radius * 2, startAngle, startAngle + currentSweep, false, false);

        // Center Value
        canvas.FontColor = Colors.White;
        canvas.FontSize = 20f;
        canvas.Font = Microsoft.Maui.Graphics.Font.DefaultBold;
        canvas.DrawString(Value.ToString("F0"), centerX, centerY - 2f, HorizontalAlignment.Center);

        // Center Unit
        canvas.FontColor = Color.FromArgb("#94A3B8");
        canvas.FontSize = 10f;
        canvas.DrawString(Unit, centerX, centerY + 16f, HorizontalAlignment.Center);
    }
}

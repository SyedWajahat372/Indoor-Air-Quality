using System;
using Microsoft.Maui.Graphics;

namespace Air_Quality.Drawables;

public class AQIGaugeDrawable : IDrawable
{
    public float Value { get; set; } = 24f;
    public float MaxValue { get; set; } = 200f;
    public string StatusText { get; set; } = "EXCELLENT";
    public Color PrimaryColor { get; set; } = Color.FromArgb("#10B981");

    public void Draw(ICanvas canvas, RectF dirtyRect)
    {
        canvas.Antialias = true;

        float width = dirtyRect.Width;
        float height = dirtyRect.Height;
        float centerX = width / 2f;
        float centerY = height / 2f;
        float radius = Math.Min(centerX, centerY) - 18f;

        float startAngle = 135f;
        float sweepAngle = 270f;

        // 1. Draw Outer Background Arc
        canvas.StrokeColor = Color.FromArgb("#1AFFFFFF");
        canvas.StrokeSize = 16f;
        canvas.StrokeLineCap = LineCap.Round;
        canvas.DrawArc(centerX - radius, centerY - radius, radius * 2, radius * 2, startAngle, startAngle + sweepAngle, false, false);

        // 2. Calculate Progress Sweep Angle
        float progressRatio = Math.Min(1f, Math.Max(0f, Value / MaxValue));
        float currentSweep = sweepAngle * progressRatio;

        // 3. Draw Active Colored Arc
        canvas.StrokeColor = PrimaryColor;
        canvas.StrokeSize = 16f;
        canvas.StrokeLineCap = LineCap.Round;
        canvas.DrawArc(centerX - radius, centerY - radius, radius * 2, radius * 2, startAngle, startAngle + currentSweep, false, false);

        // 4. Draw Radial Tick Marks
        int totalTicks = 20;
        for (int i = 0; i <= totalTicks; i++)
        {
            float tickFraction = (float)i / totalTicks;
            float angleDeg = startAngle + (sweepAngle * tickFraction);
            float angleRad = (float)(angleDeg * Math.PI / 180.0);

            float innerR = radius - 16f;
            float outerR = radius - 24f;

            float x1 = centerX + (float)(innerR * Math.Cos(angleRad));
            float y1 = centerY + (float)(innerR * Math.Sin(angleRad));
            float x2 = centerX + (float)(outerR * Math.Cos(angleRad));
            float y2 = centerY + (float)(outerR * Math.Sin(angleRad));

            canvas.StrokeColor = tickFraction <= progressRatio ? PrimaryColor : Color.FromArgb("#30FFFFFF");
            canvas.StrokeSize = 2f;
            canvas.DrawLine(x1, y1, x2, y2);
        }

        // 5. Draw Center Numeric Value
        canvas.FontColor = Colors.White;
        canvas.FontSize = 42f;
        canvas.Font = Microsoft.Maui.Graphics.Font.DefaultBold;
        canvas.DrawString(Value.ToString("F0"), centerX, centerY - 8f, HorizontalAlignment.Center);

        // 6. Draw Unit Label
        canvas.FontColor = Color.FromArgb("#94A3B8");
        canvas.FontSize = 11f;
        canvas.Font = Microsoft.Maui.Graphics.Font.Default;
        canvas.DrawString("AQI SCORE", centerX, centerY + 22f, HorizontalAlignment.Center);

        // 7. Draw Status Label
        canvas.FontColor = PrimaryColor;
        canvas.FontSize = 13f;
        canvas.Font = Microsoft.Maui.Graphics.Font.DefaultBold;
        canvas.DrawString(StatusText, centerX, centerY + 42f, HorizontalAlignment.Center);
    }
}

# Timezone Configuration Examples

This file shows example configurations for different timezones.

## India (IST - UTC+5:30)
```json
{
  "timezone": "Asia/Kolkata",
  "weekday_windows": [{"start": "07:00", "end": "23:30"}],
  "weekend_windows": [{"start": "09:00", "end": "23:30"}]
}
```
OR
```json
{
  "timezone": "IST",
  "weekday_windows": [{"start": "07:00", "end": "23:30"}],
  "weekend_windows": [{"start": "09:00", "end": "23:30"}]
}
```
OR
```json
{
  "timezone": "UTC+5.5",
  "weekday_windows": [{"start": "07:00", "end": "23:30"}],
  "weekend_windows": [{"start": "09:00", "end": "23:30"}]
}
```

## United States - Eastern Time (EST/EDT - UTC-5/-4)
```json
{
  "timezone": "EST",
  "weekday_windows": [{"start": "08:00", "end": "23:00"}],
  "weekend_windows": [{"start": "10:00", "end": "00:00"}]
}
```

## United States - Pacific Time (PST/PDT - UTC-8/-7)
```json
{
  "timezone": "PST",
  "weekday_windows": [{"start": "07:00", "end": "22:00"}],
  "weekend_windows": [{"start": "09:00", "end": "23:00"}]
}
```

## United States - Central Time (CST/CDT - UTC-6/-5)
```json
{
  "timezone": "CST",
  "weekday_windows": [{"start": "07:30", "end": "23:00"}],
  "weekend_windows": [{"start": "09:00", "end": "23:30"}]
}
```

## United Kingdom (GMT/BST - UTC+0/+1)
```json
{
  "timezone": "GMT",
  "weekday_windows": [{"start": "07:00", "end": "23:00"}],
  "weekend_windows": [{"start": "09:00", "end": "23:30"}]
}
```

## Japan (JST - UTC+9)
```json
{
  "timezone": "JST",
  "weekday_windows": [{"start": "07:00", "end": "23:00"}],
  "weekend_windows": [{"start": "09:00", "end": "23:00"}]
}
```

## Australia - Eastern (AEST - UTC+10)
```json
{
  "timezone": "AEST",
  "weekday_windows": [{"start": "07:00", "end": "23:00"}],
  "weekend_windows": [{"start": "09:00", "end": "00:00"}]
}
```

## Europe - Central (CET/CEST - UTC+1/+2)
```json
{
  "timezone": "CET",
  "weekday_windows": [{"start": "07:00", "end": "23:00"}],
  "weekend_windows": [{"start": "09:00", "end": "23:30"}]
}
```

## Custom Offset Examples

### Dubai (UTC+4)
```json
{
  "timezone": "UTC+4",
  "weekday_windows": [{"start": "07:00", "end": "23:00"}]
}
```

### Nepal (UTC+5:45)
```json
{
  "timezone": "UTC+5.75",
  "weekday_windows": [{"start": "07:00", "end": "23:00"}]
}
```

### Newfoundland (UTC-3:30)
```json
{
  "timezone": "UTC-3.5",
  "weekday_windows": [{"start": "08:00", "end": "23:00"}]
}
```

## Supported Timezone Names

The bot supports these timezone abbreviations:
- `UTC`, `GMT` - Coordinated Universal Time
- `EST`, `EDT` - US Eastern
- `CST`, `CDT` - US Central
- `MST`, `MDT` - US Mountain
- `PST`, `PDT` - US Pacific
- `IST`, `Asia/Kolkata` - India
- `JST` - Japan
- `AEST` - Australia Eastern
- `NZST` - New Zealand
- `CET`, `CEST` - Central European
- `EET` - Eastern European
- `BST` - British Summer Time

You can also use `UTC+X` or `UTC-X` format for any offset (including decimals like `UTC+5.5`).

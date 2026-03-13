using System;

namespace Portfolio.Models;

public class AboutViewModel
{
    public string Story { get; init; } = string.Empty;
    public string Formation { get; init; } = string.Empty;
    public string[] Interests { get; init; } = Array.Empty<string>();
}

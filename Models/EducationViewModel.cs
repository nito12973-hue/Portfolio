using System;

namespace Portfolio.Models;

public class EducationViewModel
{
    public string Institution { get; init; } = string.Empty;
    public string Program { get; init; } = string.Empty;
    public string[] Specializations { get; init; } = Array.Empty<string>();
}

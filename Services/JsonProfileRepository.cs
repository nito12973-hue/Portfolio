using System.IO;
using System.Text.Json;
using System.Threading;
using Microsoft.AspNetCore.Hosting;
using Portfolio.Models;

namespace Portfolio.Services;

public class JsonProfileRepository : IProfileRepository
{
    private static readonly JsonSerializerOptions SerializerOptions = new(JsonSerializerDefaults.Web) { WriteIndented = true };

    private readonly string _filePath;
    private readonly SemaphoreSlim _lock = new(1, 1);

    public JsonProfileRepository(IWebHostEnvironment environment)
    {
        var dataFolder = Path.Combine(environment.ContentRootPath, "data");
        Directory.CreateDirectory(dataFolder);
        _filePath = Path.Combine(dataFolder, "profile.json");
        if (!File.Exists(_filePath))
        {
            File.WriteAllText(_filePath, JsonSerializer.Serialize(GetDefaultProfile(), SerializerOptions));
        }
    }

    public async Task<ProfileData> GetAsync()
    {
        await _lock.WaitAsync();
        try
        {
            return await ReadUnlockedAsync();
        }
        finally
        {
            _lock.Release();
        }
    }

    public async Task SaveAsync(ProfileData profile)
    {
        await _lock.WaitAsync();
        try
        {
            await File.WriteAllTextAsync(_filePath, JsonSerializer.Serialize(profile, SerializerOptions));
        }
        finally
        {
            _lock.Release();
        }
    }

    private async Task<ProfileData> ReadUnlockedAsync()
    {
        if (!File.Exists(_filePath))
        {
            await File.WriteAllTextAsync(_filePath, JsonSerializer.Serialize(GetDefaultProfile(), SerializerOptions));
        }

        var text = await File.ReadAllTextAsync(_filePath);
        if (string.IsNullOrWhiteSpace(text))
        {
            return GetDefaultProfile();
        }

        var profile = JsonSerializer.Deserialize<ProfileData>(text, SerializerOptions);
        return profile ?? GetDefaultProfile();
    }

    private static ProfileData GetDefaultProfile() => new();
}

using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading;
using Microsoft.AspNetCore.Hosting;
using Portfolio.Models;

namespace Portfolio.Services;

public class JsonProjectRepository : IProjectRepository
{
    private static readonly JsonSerializerOptions SerializerOptions = new() { WriteIndented = true };

    private readonly string _filePath;
    private readonly SemaphoreSlim _lock = new(1, 1);

    public JsonProjectRepository(IWebHostEnvironment environment)
    {
        var dataFolder = Path.Combine(environment.ContentRootPath, "data");
        Directory.CreateDirectory(dataFolder);
        _filePath = Path.Combine(dataFolder, "projects.json");
        if (!File.Exists(_filePath))
        {
            File.WriteAllText(_filePath, JsonSerializer.Serialize(GetDefaultProjects(), SerializerOptions));
        }
    }

    public async Task<IReadOnlyList<ProjectCard>> GetAllAsync()
    {
        await _lock.WaitAsync();
        try
        {
            var list = await ReadProjectsUnlockedAsync();
            return list;
        }
        finally
        {
            _lock.Release();
        }
    }

    public async Task AddAsync(ProjectCard project)
    {
        await _lock.WaitAsync();
        try
        {
            var list = await ReadProjectsUnlockedAsync();
            list.Add(project);
            await File.WriteAllTextAsync(_filePath, JsonSerializer.Serialize(list, SerializerOptions));
        }
        finally
        {
            _lock.Release();
        }
    }

    private async Task<List<ProjectCard>> ReadProjectsUnlockedAsync()
    {
        if (!File.Exists(_filePath))
        {
            File.WriteAllText(_filePath, JsonSerializer.Serialize(GetDefaultProjects(), SerializerOptions));
        }

        var text = await File.ReadAllTextAsync(_filePath);
        if (string.IsNullOrWhiteSpace(text))
        {
            return new List<ProjectCard>();
        }

        return JsonSerializer.Deserialize<List<ProjectCard>>(text, SerializerOptions) ?? new List<ProjectCard>();
    }

    private static ProjectCard[] GetDefaultProjects() =>
        new[]
        {
            new ProjectCard(
                "SunuMarket",
                "Plateforme e-commerce pour le marché sénégalais, gérant produits, commandes et utilisateurs avec une interface fluide.",
                new[] { "Next.js", "Node.js", "MongoDB" },
                "https://github.com/lamarana/SunuMarket",
                true),
            new ProjectCard(
                "Gestion du personnel SQL",
                "Base relationnelle avec procédures stockées et rapports qui centralisent les données RH et facilitent la prise de décision.",
                new[] { "SQL Server", "Stored Procedures", "Power BI" },
                "https://github.com/lamarana/sql-personnel"),
            new ProjectCard(
                "Filtrage de nombres premiers",
                "Application Python pour générer et filtrer une suite de nombres premiers adaptée aux besoins de recherche de performances.",
                new[] { "Python", "Flask", "Pandas" },
                "https://github.com/lamarana/prime-filter"),
            new ProjectCard(
                "Refuge animalier DB",
                "Modèle de base documentaire pour gérer les animaux, les adopteurs et les campagnes, pensé pour MongoDB Atlas.",
                new[] { "MongoDB", "Aggregation", "Express" },
                "https://github.com/lamarana/refuge-db")
        };
}

using Portfolio.Models;

namespace Portfolio.Services;

public interface IProjectRepository
{
    Task<IReadOnlyList<ProjectCard>> GetAllAsync();
    Task AddAsync(ProjectCard project);
}

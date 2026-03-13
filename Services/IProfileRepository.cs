using Portfolio.Models;

namespace Portfolio.Services;

public interface IProfileRepository
{
    Task<ProfileData> GetAsync();
    Task SaveAsync(ProfileData profile);
}

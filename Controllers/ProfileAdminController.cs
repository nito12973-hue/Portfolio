using Microsoft.AspNetCore.Mvc;
using Portfolio.Filters;
using Portfolio.Models;
using Portfolio.Services;

namespace Portfolio.Controllers;

[AdminKey]
public class ProfileAdminController : Controller
{
    private readonly IProfileRepository _profileRepository;

    public ProfileAdminController(IProfileRepository profileRepository)
    {
        _profileRepository = profileRepository;
    }

    [HttpGet]
    public async Task<IActionResult> Edit()
    {
        var profile = await _profileRepository.GetAsync();
        var model = new ProfileFormModel
        {
            Name = profile.Name,
            Title = profile.Title,
            SubTitle = profile.SubTitle,
            Bio = profile.Bio,
            AvatarUrl = profile.AvatarUrl
        };

        return View(model);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(ProfileFormModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var profile = new ProfileData
        {
            Name = model.Name.Trim(),
            Title = model.Title.Trim(),
            SubTitle = model.SubTitle.Trim(),
            Bio = model.Bio.Trim(),
            AvatarUrl = string.IsNullOrWhiteSpace(model.AvatarUrl) ? "/images/avatar.svg" : model.AvatarUrl.Trim()
        };

        await _profileRepository.SaveAsync(profile);
        TempData["ProfileSaved"] = "Profil enregistré, les modifications sont visibles maintenant.";
        return RedirectToAction("Index", "Home");
    }
}

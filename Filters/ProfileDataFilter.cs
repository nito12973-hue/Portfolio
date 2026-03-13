using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Portfolio.Models;
using Portfolio.Services;

namespace Portfolio.Filters;

public class ProfileDataFilter : IAsyncActionFilter
{
    private readonly IProfileRepository _profileRepository;

    public ProfileDataFilter(IProfileRepository profileRepository)
    {
        _profileRepository = profileRepository;
    }

    public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var profile = await _profileRepository.GetAsync();
        if (context.Controller is Controller controller)
        {
            controller.ViewBag.ProfileData = profile;
        }

        await next();
    }
}

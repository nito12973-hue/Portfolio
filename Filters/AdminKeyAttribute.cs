using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Configuration;

namespace Portfolio.Filters;

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public sealed class AdminKeyAttribute : Attribute, IAsyncActionFilter
{
    private const string DefaultConfigKey = "AdminKey";

    private readonly string _configKey;

    public AdminKeyAttribute(string configKey = DefaultConfigKey)
    {
        _configKey = configKey;
    }

    public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var configuration = context.HttpContext.RequestServices.GetRequiredService<IConfiguration>();
        var expectedKey = configuration[_configKey];
        if (string.IsNullOrWhiteSpace(expectedKey))
        {
            context.Result = new UnauthorizedResult();
            return;
        }

        var providedKey = context.HttpContext.Request.Query["key"].FirstOrDefault()
                          ?? context.HttpContext.Request.Headers["X-Admin-Key"].FirstOrDefault();

        if (!string.Equals(expectedKey, providedKey, StringComparison.Ordinal))
        {
            context.Result = new UnauthorizedResult();
            return;
        }

        await next();
    }
}

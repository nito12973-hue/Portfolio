using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Portfolio.Filters;
using Portfolio.Models;
using Portfolio.Services;

namespace Portfolio.Controllers;

[AdminKey]
public class ProjectAdminController : Controller
{
    private readonly IProjectRepository _projectRepository;

    public ProjectAdminController(IProjectRepository projectRepository)
    {
        _projectRepository = projectRepository;
    }

    [HttpGet]
    public IActionResult Create()
    {
        return View(new ProjectFormModel());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(ProjectFormModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var technologies = model.Technologies.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        var project = new ProjectCard(model.Title.Trim(), model.Description.Trim(), technologies, model.Link.Trim(), model.Featured);
        await _projectRepository.AddAsync(project);
        TempData["ProjectAdded"] = $"Projet « {project.Title} » enregistré et visible dans la page Projets.";
        return RedirectToAction("Projects", "Home");
    }
}

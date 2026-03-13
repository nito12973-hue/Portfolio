using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Portfolio.Models;
using Portfolio.Services;

namespace Portfolio.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly IProjectRepository _projectRepository;

    private static readonly SkillCategory[] SkillCategories =
    {
        new("Langages", new[] { "HTML", "CSS", "JavaScript", "Python", "SQL" }, "bi-code-slash"),
        new("Frameworks", new[] { "ASP.NET", "Django", "React / Next.js" }, "bi-braces"),
        new("Bases de données", new[] { "MySQL", "PostgreSQL", "MongoDB" }, "bi-database"),
        new("Administration de bases de données", new[] { "Monitoring", "Sécurité des accès", "Optimisation de performances" }, "bi-hdd-network")
    };

    private const string GithubLink = "https://github.com/lamarana";
    private const string ContactEmail = "lamaranamamadousdiallo@gmail.com";
    private const string ContactPhone = "+221775365983";

    public HomeController(ILogger<HomeController> logger, IProjectRepository projectRepository)
    {
        _logger = logger;
        _projectRepository = projectRepository;
    }

    public async Task<IActionResult> Index()
    {
        var projects = await _projectRepository.GetAllAsync();
        var featured = projects.FirstOrDefault(p => p.Featured) ?? projects.FirstOrDefault();
        ViewBag.FeaturedProject = featured;
        return View();
    }

    public IActionResult About()
    {
        var model = new AboutViewModel
        {
            Story = "Bonjour, je suis Lamarana Diallo, étudiant en informatique et administrateur de bases de données passionné par le développement web et mobile.",
            Formation = "Actuellement en licence informatique, je complète ma formation avec des projets full-stack, des applications mobiles et des stratégies de gestion des données.",
            Interests = new[]
            {
                "Développement web",
                "Bases de données",
                "Systèmes d’exploitation",
                "Applications mobiles"
            }
        };
        return View(model);
    }

    public IActionResult Skills()
    {
        return View(SkillCategories);
    }

    public async Task<IActionResult> Projects()
    {
        var projects = await _projectRepository.GetAllAsync();
        ViewBag.ProjectAdded = TempData["ProjectAdded"] as string;
        return View(projects.OrderByDescending(p => p.Featured));
    }

    public IActionResult Education()
    {
        var model = new EducationViewModel
        {
            Institution = "Université de Dakar",
            Program = "Licence en informatique",
            Specializations = new[]
            {
                "Bases de données",
                "Systèmes d’exploitation",
                "Développement web"
            }
        };
        return View(model);
    }

    public IActionResult Contact()
    {
        SetContactLinks();
        if (TempData["ContactSuccess"] is string success)
        {
            ViewBag.ContactSuccess = success;
        }

        return View(new ContactFormModel());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Contact(ContactFormModel form)
    {
        SetContactLinks();
        if (!ModelState.IsValid)
        {
            return View(form);
        }

        TempData["ContactSuccess"] = "Votre message a bien été envoyé. Je reviens vers vous rapidement.";
        return RedirectToAction(nameof(Contact));
    }

    private void SetContactLinks()
    {
        ViewBag.GithubLink = GithubLink;
        ViewBag.ContactEmail = ContactEmail;
        ViewBag.ContactPhone = ContactPhone;
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}

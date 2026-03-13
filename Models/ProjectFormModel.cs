using System.ComponentModel.DataAnnotations;

namespace Portfolio.Models;

public class ProjectFormModel
{
    [Required(ErrorMessage = "Le titre est requis.")]
    public string Title { get; set; } = string.Empty;

    [Required(ErrorMessage = "La description est requise.")]
    public string Description { get; set; } = string.Empty;

    [Required(ErrorMessage = "Ajoute au moins une technologie.")]
    public string Technologies { get; set; } = string.Empty;

    [Required(ErrorMessage = "Le lien du projet est requis.")]
    [Url(ErrorMessage = "Le lien doit être une URL valide.")]
    public string Link { get; set; } = string.Empty;

    public bool Featured { get; set; }
}

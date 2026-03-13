using System.ComponentModel.DataAnnotations;

namespace Portfolio.Models;

public class ProfileFormModel
{
    [Required(ErrorMessage = "Le nom est requis.")]
    public string Name { get; set; } = string.Empty;

    [Required(ErrorMessage = "Le titre est requis.")]
    public string Title { get; set; } = string.Empty;

    [Required(ErrorMessage = "Le sous-titre est requis.")]
    public string SubTitle { get; set; } = string.Empty;

    [Required(ErrorMessage = "La bio est requise.")]
    public string Bio { get; set; } = string.Empty;

    [Url(ErrorMessage = "L’URL de l’avatar doit être valide.")]
    public string AvatarUrl { get; set; } = string.Empty;
}

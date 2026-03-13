using System.ComponentModel.DataAnnotations;

namespace Portfolio.Models;

public class ContactFormModel
{
    [Required(ErrorMessage = "Le nom est requis.")]
    public string Name { get; set; } = string.Empty;

    [Required(ErrorMessage = "L’email est requis.")]
    [EmailAddress(ErrorMessage = "Email invalide.")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Un message est requis.")]
    [StringLength(1000, ErrorMessage = "Le message ne peut dépasser 1 000 caractères.")]
    public string Message { get; set; } = string.Empty;
}

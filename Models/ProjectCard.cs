namespace Portfolio.Models;

public record ProjectCard(string Title, string Description, string[] Technologies, string Link, bool Featured = false);

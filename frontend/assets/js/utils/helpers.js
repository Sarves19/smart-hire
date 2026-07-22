/**
 * ==========================================================
 * Smart Hire Helper Functions
 * ==========================================================
 */

/**
 * Generate initials from a full name.
 *
 * Example:
 * "Sarves Suresh" -> "SS"
 * "John David" -> "JD"
 */

function getInitials(name) {

    if (!name) return "?";

    return name
        .trim()
        .split(" ")
        .filter(word => word.length > 0)
        .map(word => word[0].toUpperCase())
        .slice(0, 2)
        .join("");

}


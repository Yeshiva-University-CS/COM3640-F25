using System.Runtime.CompilerServices;

[assembly: InternalsVisibleTo("ClinicalTrials.Tests")]

namespace ClinicalTrials.Domain.Models;

/// <summary>
/// Partial class containing internal test constructor for ClinicalTrial.
/// This constructor bypasses all validation and allows creating trials in any state.
/// ONLY for use by test scenarios - never use in production code.
/// </summary>
public partial class ClinicalTrial
{
    /// <summary>
    /// Internal constructor for test scenarios only.
    /// Allows creating a trial in any intermediate state without validation.
    /// </summary>
    /// <remarks>
    /// This constructor is exposed to the test assembly via InternalsVisibleTo.
    /// It enables test scenario factories to create trials at specific lifecycle points.
    /// </remarks>
    internal ClinicalTrial(bool temp)
    {
        // TODO: Implement test constructor, adding parameters as needed
        // Direct assignment of all fields without validation
        // This bypasses business rules to enable testing intermediate states
        // Add parameters as needed. (temp parameter is a placeholder and can be removed)
        throw new NotImplementedException();
    }
}

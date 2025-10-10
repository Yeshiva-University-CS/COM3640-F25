using ClinicalTrials.Domain.Models;

namespace ClinicalTrials.Tests.Scenarios;

/// <summary>
/// Factory class for creating ClinicalTrial instances in various test scenarios.
/// Uses internal test constructors to bypass validation and create intermediate states.
/// </summary>
public static class TrialScenarios
{
    /// <summary>
    /// Creates a trial in Planning state, ready to transition to Recruiting.
    /// Target enrollment is set and all planning is complete.
    /// </summary>
    public static ClinicalTrial PlanningReadyForRecruiting()
    {
        throw new NotImplementedException();
    }

    /// <summary>
    /// Creates a trial in Recruiting state with target enrollment reached.
    /// All accepted participants have baseline visits recorded.
    /// Ready to transition to Active.
    /// </summary>
    public static ClinicalTrial RecruitingTargetReached()
    {
        throw new NotImplementedException();
    }

    /// <summary>
    /// Creates a trial in Active state with participants randomized.
    /// Some follow-up visits recorded, but not all participants have completed Final visit.
    /// </summary>
    public static ClinicalTrial ActiveWithPartialData()
    {
        throw new NotImplementedException();
    }

    /// <summary>
    /// Creates a trial in Active state ready to transition to Completed.
    /// All participants have all required visits including Final.
    /// </summary>
    public static ClinicalTrial ActiveReadyForCompletion()
    {
        throw new NotImplementedException();
    }

    /// <summary>
    /// Creates a trial in Completed state with all data collected.
    /// Ready for outcome analysis.
    /// </summary>
    public static ClinicalTrial CompletedReadyForAnalysis()
    {
        throw new NotImplementedException();
    }

    /// <summary>
    /// Creates a trial in Recruiting state that should terminate.
    /// Has screened 2x target enrollment without reaching target of accepted participants.
    /// </summary>
    public static ClinicalTrial RecruitingShouldTerminate()
    {
        throw new NotImplementedException();
    }
}

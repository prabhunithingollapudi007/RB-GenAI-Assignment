# Qualitative Evaluation Report  

**Scope of this Report**  
This document covers the qualitative dimensions of the evaluation only:  
- Key Informational Units / Fact Consistency  
- Lifestyle & Demographic Congruence  
- Linguistic & Stylistic Authenticity  
- Holistic Advanced Reasoning LLM Judgment

---

## 1. Dataset and Findings Summary

**Source file:** `paired_answers_clean.csv`

| Person ID  | Profile Summary (from answers)                          | Number of Questions |
|------------|---------------------------------------------------------|---------------------|
| c_human    | Pragmatic, low brand involvement, price/function-focused, online + occasional store | 10 |
| s_human    | Korean skincare enthusiast, ingredient-conscious, oily/acne-prone, clear channel split | 10 |
| g_human    | High convenience orientation, low involvement, supermarket-centric, design > ingredients | 10 |


**Key Findings:**

- **Overall holistic score:** ~2.9 / 5
- **Best performer:** s_human (high product knowledge, Korean skincare) – average ~3.7
- **Weaker performers:** c_human (~2.6) and g_human (~2.3) – both lower-involvement profiles

---

## 2. Key Informational Units / Fact Consistency

Atomic claims, constraints, preferences, and explicit rejections were extracted from each Human Answer and compared against the corresponding AI Answer.

### Summary Table by Person

| Person     | Strong Matches | Partial / Soft Matches | Clear Omissions or Contradictions | Inventions / Unsupported Details |
|------------|----------------|------------------------|-----------------------------------|----------------------------------|
| **c_human** | Low–Moderate  | Moderate              | High                             | Moderate–High                   |
| **s_human** | High (products & channels) | Moderate         | Moderate                         | Moderate (extra detail)         |
| **g_human** | Moderate (convenience & low brand attention) | Moderate | High (bulk buying & travel packaging) | High                            |

### Detailed Findings by Person

#### c_human
**Well captured**
- Preference for online purchasing (flexibility + discounts)
- Occasional in-store impulse buys
- Low brand knowledge (“I don’t really know the brands”)
- Focus on products that “get the job done” and are affordable
- Long-term toothpaste inertia (continued from family habit)
- Discovery via friends and Instagram

**Major mismatches**
- Human explicitly avoids bulk buying (“I don’t usually buy in bulk, but rather as soon as I need them”). AI invents regular bulk purchasing of toothpaste and deodorant.
- Celebrity preference: Human wants a handsome, lean male movie star (Jacob Elordi / Christian Bale). AI selects Emma Watson on sustainability grounds - complete mismatch.
- Ideal body wash: Human emphasizes effectiveness + affordability + sustainable ingredients. AI expands into specific botanicals, absence of sulfates/parabens, and eco-packaging (reasonable extrapolation but more detailed than the source).

**Overall pattern:** AI makes the person appear more deliberate and sustainability-oriented than the human answers indicate.

#### s_human
**Well captured**
- Precise product knowledge: YesStyle, Some By Mi, Axis-Y, Beauty of Joseon
- Clear channel split (Korean face products online vs body care at supermarket/DM)
- Value placed on ingredient transparency, free samples, natural/organic options
- Packaging preference (large size, glass, transparent, minimalistic) is directionally correct

**Major mismatches**
- Bulk buying: Human only bulk-buys body/hand wash and explicitly dislikes large face/hair sizes. AI invents bulk purchasing of the exact Korean face products the human uses.
- Celebrity: Human casually names Keira Knightley. AI selects Hyram Yarbro (skincare influencer) more “on-brand” but not what was stated.
- Perfect body wash: Human requests full ingredient transparency with effect explanations, clear glass bottle, soft-not-heavy texture, and oud scent. AI produces a generic organic formula and misses the oud and detailed labeling request.

**Overall pattern:** Strongest factual grounding in the sample, especially on concrete product and channel details. Still tends to add extra justification and occasionally invents behavior.

#### g_human
**Well captured**
- Supermarket as primary, convenience-driven channel
- Low brand awareness and attention
- Rotating toothpaste brands without strong loyalty
- Preference for visual design over product names
- Discovery mainly through in-store chance encounters
- Absence of a single favorite brand

**Major mismatches**
- Bulk buying: Human almost never buys bulk (only rare discounted doubles). AI invents regular bulk buying of Head & Shoulders and Nivea deodorant.
- Packaging: Human clearly distinguishes home use (medium-large metal >300 ml, refillable pump, minimalistic) from travel (small ~150 ml plastic). AI collapses this into a single 500 ml simple bottle and ignores the travel distinction.
- Celebrity: Human cannot think of a male celebrity and notes they appear polished/made-up. AI selects David Beckham.
- Perfect body wash: Human has no ingredient preferences and only cares about pleasant smell + not drying the skin. AI invents specific ingredients (peppermint, shea butter) and a refillable-pump narrative.

**Overall pattern:** AI systematically increases involvement, brand loyalty, and bulk behavior beyond what the human expressed.

### Cross-Person Pattern
Across all three individuals the simulations frequently:
- Invent or exaggerate bulk-buying behavior
- Elevate sustainability and ingredient consciousness
- Supply specific justifications even when the human expressed indifference or uncertainty

---

## 3. Lifestyle & Demographic Congruence

**Target segment definition:** Young business professionals who work long hours and travel frequently.

| Dimension                     | c_human                  | s_human                          | g_human                          | AI Behavior Across Persons |
|-------------------------------|--------------------------|----------------------------------|----------------------------------|----------------------------|
| Time / convenience focus      | Present (online flexibility) | Moderate                        | Strong (supermarket one-stop)    | AI amplifies convenience language |
| Travel-related needs          | Absent                   | Absent                           | Explicit (small travel bottles)  | Almost completely ignored for g_human |
| Professional image / long hours | Not mentioned           | Not mentioned                    | Not mentioned                    | AI does not inject these either |
| Sustainability / values       | Light                    | Strong (ingredients, organic)    | Weak                             | AI systematically elevates sustainability |

**Key observations**
- The human answers contain relatively few strong signals of extreme time poverty or high travel frequency.
- The agents do **not** force a heavy “busy professional traveler” stereotype, which is positive.
- However, they fail to preserve the one clear travel-related signal that does exist (g_human’s dual home vs travel packaging preference).
- Sustainability language is injected more strongly than most human answers support, likely reflecting model priors rather than individual self-reports.

---

## 4. Linguistic & Stylistic Authenticity

| Feature                     | Human Pattern                                      | AI Pattern                                          | Match Quality   |
|-----------------------------|----------------------------------------------------|-----------------------------------------------------|-----------------|
| Length & elaboration        | Often short, incomplete sentences, casual          | Consistently longer, more structured paragraphs     | Poor            |
| Certainty / hedging         | Frequent “I don’t know”, “I think”, “not 100%”, “rather likely” | More assertive and explanatory                 | Poor            |
| Brand knowledge expression  | Explicit uncertainty or indifference               | Fills in specific brands and rationales             | Poor            |
| Emojis / tone               | None                                               | Occasional 😊 (mainly s_human)                      | Minor mismatch  |
| First-person voice          | Present                                            | Present                                             | Good            |
| Specificity vs vagueness    | Mix; often vague on brands                         | Tends toward concrete examples and justifications   | Moderate–Poor   |

**Overall stylistic verdict**  
AI answers are noticeably more polished, complete, and “market-research ready.” Human answers are more fragmentary, uncertain, and low-effort in places. The simulations reduce the natural messiness and indifference that characterize real low-involvement responses.

---

## 5. Holistic Advanced Reasoning LLM Judgment

**Scoring scale**  
5 = Would convincingly pass as the same person on a blind read  
4 = Strong core match with only minor additions  
3 = Recognizable core but noticeable shifts in involvement or details  
2 = Partial overlap; important preferences distorted  
1 = Largely different persona

| Person     | Average Score | Commentary |
|------------|---------------|------------|
| **c_human** | 2.6          | Core pragmatism and low brand involvement partially preserved, but bulk-buying invention, celebrity mismatch, and elevated sustainability pull the score down. |
| **s_human** | 3.7          | Best overall. Product knowledge and channel split are well captured. Bulk-buying and celebrity choices are the main distortions. |
| **g_human** | 2.3          | Convenience and low involvement remain visible, but travel packaging, bulk behavior, and ingredient indifference are poorly handled. AI makes the person more deliberate than the source answers suggest. |

**Overall average across all pairs: ≈ 2.9 / 5**

---

## 6. Strengths of the Simulations

- Strong capture of concrete product knowledge and shopping channels when these are clearly present in the human answers (especially s_human).
- Reasonable preservation of broad convenience orientation and supermarket / online channel preferences.
- Answers remain in first-person voice and stay generally on-topic.
- The agents do not over-apply a forced “busy traveler / high-powered professional” stereotype that is largely absent from the source data.

---

## 7. Weaknesses & Recurring Failure Modes

1. **Invention of bulk-buying behavior**  
   Appears across all three people, even when humans explicitly reject or rarely engage in bulk purchasing.

2. **Elevated involvement and justification**  
   AI supplies reasons, brand loyalty statements, and sustainability language that the humans often lack.

3. **Loss of uncertainty and low-effort signals**  
   Humans frequently express indifference (“I don’t know”, “I don’t care”, “I just continued what my mum bought”). AI rarely mirrors this.

4. **Ignoring dual-context or situational preferences**  
   Clearest example: g_human’s distinction between home (large metal, refillable) and travel (small plastic) packaging is collapsed.

5. **Replacement of casual or uncertain choices**  
   Celebrity and aspirational preferences are systematically replaced with more “on-brand” or values-aligned figures.

6. **Stylistic homogenization**  
   All AI answers become longer, more fluent, and more complete than the human originals.

These patterns are consistent with known LLM tendencies: filling in plausible detail, reducing expressed uncertainty, and aligning with socially desirable or sustainability-oriented priors.

---

## 8. Recommendations

**For agent construction**
- Enrich the grounding interviews with explicit probes on bulk-buying habits, travel routines, brand indifference, and situational (home vs travel) preferences.
- Add generation-time constraints that instruct the model to preserve stated uncertainty and explicit rejections.

**For evaluation design**
- Flag answers that express indifference or uncertainty and penalize the agent for overriding them.
- Introduce preference-ranking or forced-choice tasks alongside open-ended questions for more objective scoring.
- Collect human test-retest data on the evaluation questions so performance can be normalized against individual consistency ceilings (as in the original paper).

**For commercial use**
- Current agents appear more reliable for higher-involvement consumers (e.g., s_human profile).
- They risk misrepresenting the large low-involvement segment that buys primarily on convenience and habit.
- Downstream utility testing is recommended: can product teams generate better insights or hypotheses from the agents than from traditional research methods?

---

## 9. Limitations of this Evaluation

- Extremely small sample (n = 3) → results are illustrative rather than statistically powered.
- No access to the original interview transcripts used to build the agents → cannot fully diagnose whether failures originate in grounding data or in generation behavior.
- No human test-retest reliability on these exact questions → cannot apply the consistency-ceiling normalization used in the reference paper.
- Single-turn open-ended answers are inherently noisy; multi-turn or structured tasks would strengthen conclusions.

---

## 10. How to Reproduce / Extend

1. Load `paired_answers_clean.csv`.
2. For each Human–AI pair:
   - Extract atomic claims from the human answer.
   - Code the AI answer as match / partial / omit / contradict / invent.
3. Apply the lifestyle checklist and stylistic comparison.
4. Assign holistic 1–5 scores with short rationales.
5. Aggregate by person and by question category.

For larger datasets, the fact-consistency step can be partially automated with LLM-assisted claim extraction + human verification.
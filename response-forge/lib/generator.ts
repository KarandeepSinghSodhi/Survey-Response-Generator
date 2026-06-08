export type SyntheticResponse = {
  id: number;
  satisfaction: number;
  nps: number;
  category: string;
  delivery: "Yes" | "No";
  feedback: string;
  persona: string;
};

const CATEGORIES = ["Electronics", "Clothing", "Home", "Other"];
const PERSONAS = [
  "Value Seeker",
  "Trend Seeker",
  "Home Comfort Shopper",
  "Delivery-Sensitive Shopper",
];

const weightedChoice = <T,>(options: readonly T[], weights: number[]) => {
  const total = weights.reduce((sum, value) => sum + value, 0);
  let threshold = Math.random() * total;
  for (let i = 0; i < options.length; i += 1) {
    threshold -= weights[i];
    if (threshold <= 0) return options[i];
  }
  return options[options.length - 1];
};

const clamp = (value: number, min = 0, max = 1) => Math.min(max, Math.max(min, value));

const makeProfile = () => {
  const ageGroups = ["18-24", "25-34", "35-44", "45-54", "55+"];
  const incomes = ["low", "medium", "high"] as const;
  const frequencies = ["low", "medium", "high"] as const;

  const ageGroup = weightedChoice(ageGroups, [0.14, 0.32, 0.24, 0.18, 0.12]);
  const income = weightedChoice(incomes, [0.30, 0.45, 0.25]);
  const frequency = weightedChoice(frequencies, [0.24, 0.48, 0.28]);
  const techSavviness = clamp((Math.random() * 0.18) + (ageGroup === "18-24" ? 0.75 : ageGroup === "25-34" ? 0.70 : ageGroup === "35-44" ? 0.60 : ageGroup === "45-54" ? 0.50 : 0.40));

  const personaBase = [0.30, 0.25, 0.25, 0.20];
  if (income === "high") {
    personaBase[0] = 0.20;
    personaBase[1] = 0.35;
    personaBase[2] = 0.22;
    personaBase[3] = 0.23;
  } else if (income === "low") {
    personaBase[0] = 0.40;
    personaBase[1] = 0.15;
    personaBase[2] = 0.30;
    personaBase[3] = 0.15;
  }
  if (techSavviness > 0.7) {
    personaBase[0] -= 0.05;
    personaBase[1] += 0.10;
  }
  if (frequency === "high") {
    personaBase[3] += 0.08;
    personaBase[2] -= 0.03;
  }

  const persona = weightedChoice(PERSONAS, personaBase.map((value) => Math.max(0.05, value)));

  return { ageGroup, income, frequency, techSavviness, persona };
};

const chooseCategory = (persona: string, techSavviness: number, income: string, frequency: string) => {
  const weights = [0.18, 0.20, 0.24, 0.38];
  if (techSavviness > 0.7) {
    weights[0] += 0.15;
    weights[3] -= 0.05;
  }
  if (income === "high") {
    weights[0] += 0.08;
    weights[1] -= 0.04;
  }
  if (frequency === "high") {
    weights[2] += 0.06;
  }

  if (persona === "Trend Seeker") {
    weights[0] += 0.15;
    weights[1] += 0.05;
  }
  if (persona === "Home Comfort Shopper") {
    weights[2] += 0.18;
  }
  if (persona === "Delivery-Sensitive Shopper") {
    weights[3] += 0.08;
  }

  return weightedChoice(CATEGORIES, weights.map((value) => Math.max(0.02, value)));
};

const buildFeedback = ({ satisfaction, delivery, category, persona }: { satisfaction: number; delivery: "Yes" | "No"; category: string; persona: string; }) => {
  const goodDelivery = delivery === "Yes";
  const positive = satisfaction >= 4;
  const templates = [
    `I appreciated how quickly the ${category.toLowerCase()} item arrived and it matched the description well.`,
    `The experience felt polished, especially since delivery was on time and the product quality was strong.`,
    `I enjoyed the value for money and the order was handled smoothly from checkout to delivery.`,
    `The product arrived before I expected it, and I’m happy with how it performs.`,
    `Delivery was a highlight, but I’d love more polish on product packaging next time.`,
    `Everything worked well on the order, though the item could be a bit more impressive for the price.`,
    `The purchase was solid, but I think the experience would improve with faster updates on shipping status.`,
    `I liked the item overall, though the delivery updates were a little light this time.`,
    `It was an easy experience, but the product felt slightly underwhelming for the category.`,
    `The package arrived late and that made the whole order feel less reliable.`,
    `Shipping delays hurt the otherwise good product quality.`,
    `I got what I needed, but the late delivery made the experience frustrating.`,
    `The item was okay, but the shipping timeline was disappointing.`,
    `Delivery missed the window and it made the whole purchase feel rushed.`,
  ];

  if (positive && goodDelivery) {
    return templates[0];
  }
  if (positive && !goodDelivery) {
    return templates[7];
  }
  if (!positive && goodDelivery) {
    return templates[5];
  }
  return templates[10];
};

const getResponseFromScore = (score: number, deliveryOnTime: boolean) => {
  let satisfaction: number;
  let nps: number;

  if (score > 0.8) {
    satisfaction = 5;
    nps = Math.floor(Math.random() * 3) + 8;
  } else if (score > 0.6) {
    satisfaction = 4;
    nps = Math.floor(Math.random() * 3) + 7;
  } else if (score > 0.4) {
    satisfaction = 3;
    nps = Math.floor(Math.random() * 3) + 5;
  } else if (score > 0.2) {
    satisfaction = 2;
    nps = Math.floor(Math.random() * 4) + 2;
  } else {
    satisfaction = 1;
    nps = Math.floor(Math.random() * 4);
  }

  if (!deliveryOnTime && satisfaction === 5) {
    satisfaction = 4;
  }

  if (deliveryOnTime && nps < 5 && satisfaction >= 4) {
    nps = Math.max(nps, 7);
  }

  return { satisfaction, nps };
};

export const generateSyntheticResponses = (count: number) => {
  return Array.from({ length: count }, (_, index) => {
    const profile = makeProfile();
    const category = chooseCategory(profile.persona, profile.techSavviness, profile.income, profile.frequency);
    const deliveryChance = clamp(0.78 + 0.08 * (profile.frequency === "low" ? 1 : 0) - 0.12 * (profile.persona === "Delivery-Sensitive Shopper" ? 1 : 0));
    const deliveryOnTime = Math.random() < deliveryChance;
    const productScore = clamp(0.46 + 0.22 * (profile.techSavviness > 0.68 ? 1 : 0) + 0.16 * (profile.persona === "Trend Seeker" ? 1 : 0) + (category === "Electronics" ? 0.08 : category === "Home" ? 0.05 : 0));
    const deliveryScore = clamp(deliveryOnTime ? 0.84 : 0.36);
    const priceScore = clamp(0.43 + 0.24 * (profile.income === "high" ? 1 : 0) - 0.11 * (profile.persona === "Value Seeker" ? 1 : 0));
    const satisfactionSignal = clamp(0.48 * productScore + 0.28 * deliveryScore + 0.24 * priceScore + (Math.random() * 0.06 - 0.03));

    const { satisfaction, nps } = getResponseFromScore(satisfactionSignal, deliveryOnTime);
    const feedback = buildFeedback({ satisfaction, delivery: deliveryOnTime ? "Yes" : "No", category, persona: profile.persona });

    return {
      id: index + 1,
      satisfaction,
      nps,
      category,
      delivery: deliveryOnTime ? "Yes" : "No" as "Yes" | "No",
      feedback,
      persona: profile.persona,
    };
  });
};

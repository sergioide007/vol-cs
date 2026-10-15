# Chapter 28: Soccer and Multi-Agent Systems: Where the Tactical Future Emerges

> *In soccer, 11 players are 11 agents. Tactics are agentic emergence; the coach is the orchestrator.*

## The Match as a Multi-Agent System: A Theoretical Formalization

Before applying the term "multi-agent system" to soccer, it needs a precise definition, because the connection is structural, not metaphorical. In the canonical definition of Wooldridge and Jennings (1995), a multi-agent system is a system made up of multiple autonomous agents that perceive their environment, reason about what they perceive, and act in coordination (or in competition) to reach individual or collective goals. A soccer match meets each of those criteria with more precision than most artificial software systems do.

Each player is an agent that: (a) perceives the environment (ball position, teammates' and opponents' positions, the score, time remaining); (b) keeps an internal model of the world (expectations about the opposing coach's behavior, knowledge of teammates' strengths, an understanding of the constraints of the tactical system); (c) makes decisions in real time under severe time pressure (an elite player's decision window is a fraction of a second *[order of magnitude: optical tracking samples at a high frequency precisely because a human cannot process every frame, but the size of the decision window is not cited here because it depends on the sport, the position, and the level; measure it on your own team]*); and (d) coordinates with other agents on the same team through implicit protocols, the shared tactical language that defines what the left winger does when the holding midfielder receives the ball with pressure from behind.

This formalization is not trivial. It means the theoretical tools developed for artificial multi-agent systems (game theory, consensus protocols, MARL) apply *directly* to tactical analysis and optimization in soccer, as formal frameworks and not as analogies.

## The Data Layer: From Events to Biomechanical Tracking

Soccer analysis has gone through three generations of data, which correspond, not by chance, to the three generations of multi-agent analysis.

**First generation: event data.** Until about 2012, standard analysis relied on event data: completed passes, shots on target, distance covered, fouls committed. This data captures *what* happened, not *how* or *why*. It is the equivalent of an application log in software systems: useful for post-mortem diagnosis, not enough for causal inference.

**Second generation: 2D tracking.** Between 2012 and 2020, elite leagues (notably the Premier League, the Bundesliga, and Serie A) began deploying optical tracking systems that record the position of every player and the ball at 25 frames per second. Tracab (ChyronHego), Second Spectrum, and Stats Perform lead this segment. With 2D tracking data, it is possible to compute metrics that event data cannot capture: pressing speed, space available at the moment of the pass, and defensive coverage as a function of the positions of all players at once. The public dataset most used in academic research is the one published by Pappalardo et al. (2019) in Nature's *Scientific Data*; it provides spatiotemporal events from five European leagues and has been downloaded more than 50,000 times since publication.

**Third generation: biomechanical and multimodal tracking.** In 2023–2025, a small number of clubs (Liverpool FC, Manchester City, and Bayern Munich are among the documented cases) began experimenting with systems that combine optical tracking with biomechanical data from advanced GPS units and body-worn accelerometers. With this data, the unit of analysis stops being position on the pitch and becomes the agent's *physiological and cognitive state*: level of muscle fatigue, acceleration and deceleration patterns, and response to visual stimuli. The analytical consequence is substantial: you can predict when an agent is cognitively overloaded before visible performance degrades.

## The Technical Architecture: MARL on the Pitch

**► TECHNICAL TRACK**


### Vision Agents: Real-Time Tracking

The first layer of the agentic analysis system is the *vision agent*: a computer vision model that extracts the position and state of every player in real time from the video feed or tracking sensors. In production implementations (such as those Stats Perform has deployed in the Premier League), this agent processes 25 frames per second with latency under 40 milliseconds, which allows truly real-time analysis during the match.

The technical difficulty is not in detecting players (a YOLO-style model can do that) but in *persistent identification*: keeping the identity of player #7 across occlusions, visual collisions between players, and camera changes. This persistence of identity is the multi-object tracking (MOT) problem, and solving it is the prerequisite for any meaningful tactical analysis.

### Decision Agents: Reasoning About Space and Possession

On top of the tracking data, a second layer of agents reasons about higher-level tactical concepts: space, pressure, available passing lanes, and defensive coverage zones. The seminal work of Fernández and Bornn (2018), *Wide Open Spaces: A statistical technique for measuring space creation in professional soccer*, formalizes each player's "space of influence" as a function of their position, their velocity, and the positions of every other agent on the pitch. This metric (called pitch control in the literature) makes it possible to quantify in real time what fraction of the field each team controls and how that distribution changes with every movement.

The agentic extension of this work turns the pitch control calculation into a reactive agent that updates its state every frame: the *spatial control agent*, which produces a real-time heat map of tactical influence. Combined with the *pressure agent* (which quantifies how much time the ball carrier has before being closed down, based on the defenders' speeds and positions), these agents produce a quantitative description of the match's tactical state that no human analyst can compute in real time.

### The Action Valuation Agent: Beyond the Goal

The most powerful metric in multi-agent soccer analysis is *action valuation*: how much value each individual action adds to or subtracts from the probability of scoring. The paper by Decroos et al. (2019), *Actions Speak Louder Than Goals: Valuing Player Actions in Soccer* (published at KDD 2019, the most selective data mining conference), introduces the VAEP framework (Valuing Actions by Estimating Probabilities), which quantifies the value of any action, not just goals and assists, as a change in the probability of scoring or conceding.

The VAEP system is multi-agent in structure. A context agent extracts features of the game state before and after each action, a valuation agent computes the change in goal probability, and an attribution agent assigns that change to the player who performed the action. Together, these agents produce a quantitative description of *who contributed what, and when*, with a precision that no conventional statistics system can match.

## Documented Cases: Clubs Already Deploying Multi-Agent Systems

### Liverpool FC: The Research Department as a Competitive Advantage

Over the last decade, Liverpool FC has built a research and analytics department that the soccer industry recognizes as the benchmark for applying data science to sporting decisions. The work of Ian Graham (a mathematician with a doctorate in computational physics from Cambridge), the club's Director of Research from 2012 to 2022, established a methodology based on probabilistic models for player evaluation, tactical analysis, and opponent preparation.

Liverpool's analysis system is not multi-agent in the strict technical sense of a pipeline of software agents. It is multi-agent in the organizational sense: multiple analytical agents, human and algorithmic, work on shared data, produce independent analyses, and synthesize them into recommendations for the coaching staff. The separation between the tactical analysis agent (which studies the opponent's patterns of play) and the player valuation agent (which evaluates the transfer market), with synthesis done by a human orchestrator, is structurally identical to the multi-agent architecture pattern described in Chapter 8.

### StatsBomb: The Company That Turned Data into Agentic Knowledge

StatsBomb (founded in 2012 by Ted Knutson) has built the highest-resolution soccer event database that is publicly available. StatsBomb's data model captures not only the type of event (pass, shot, tackle) but its tactical context: the body part used, the 3D position of the ball at the moment of contact, a pressure indicator on the ball carrier, and the movement pattern before the pass. That granularity turns each event into a state vector that can feed a MARL model directly.

Academic research that has used StatsBomb data includes papers published at KDD, sports analytics workshops at NeurIPS, and the MIT Sloan Sports Analytics Conference. Public access to data from the Women's World Cup and national team competitions has let researchers at many universities develop and compare tactical analysis models reproducibly, a standard of rigor that traditional soccer analysis had never reached.

### Bayern Munich: A Digital Twin of Tactics

Bayern Munich, working with SAP technology, has developed a tactical analysis system that the club's own materials call a "digital twin of tactics": a computational representation of the team's tactical system that can simulate how it would respond to variations, new starting positions, substitutions, and changes in the opponent's formation. In essence, this simulation is a multi-agent system: each player is represented by an agent with a behavior model learned from historical data, and the tactics emerge from the interaction of those agents in the simulation.

## Multi-Agent Reinforcement Learning (MARL): The State of the Research

The state of the art in MARL applied to team sports was settled by Vinyals et al. (2019), *Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning* (published in *Nature*, volume 575), in which a multi-agent architecture based on reinforcement learning reached grandmaster level in StarCraft II (a strategy game with imperfect information and team dynamics) without expert-designed heuristics. The lessons from that work transfer directly to soccer analysis: the challenges of coordinating units, exploring the strategy space, and generalizing to opponents not seen in training are structurally the same in both domains.

The QMIX framework by Rashid et al. (2018), published at *ICML 2018*, shows how to factor a swarm's Q-value into individual Q-values so that the centralized policy stays consistent with decentralized execution. This architecture, called CTDE (Centralized Training with Decentralized Execution), is directly relevant to soccer analysis: the model is trained with access to all the data (complete tracking of every player), but at inference time each agent decides based only on its own local observation.

The work of Lowe et al. (2017), *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments* (NeurIPS 2017), extends the classic actor-critic to environments where agents are cooperative with teammates and competitive with opponents at the same time, which is exactly the dynamic of a soccer match. The policy gradients learned in that framework capture the balance between maximizing an agent's individual payoff and contributing to the team's collective success. In soccer, that shows up as the tension between the player chasing individual glory by shooting and the one who passes to the better-positioned teammate.

## The Executive View: Player Valuation and Risk Management

**■ EXECUTIVE TRACK**


For organizational leaders, multi-agent analysis in soccer has quantifiable business implications that go beyond improving sporting performance.

**Market valuation.** Action valuation models (VAEP, Expected Threat, Expected Goals) have transformed the transfer market. A club that can measure precisely what a player is really worth, separating individual contribution from the tactical system the player operates in, has an information advantage in transfer negotiations. The return on investment of these analytical capabilities has been documented: clubs that adopted advanced data analytics before 2015 showed transfer market performance that was consistently above their league average over the 2015–2022 period (an analysis documented by the company 21st Club).

**Injury risk management.** High-frequency biomechanical data can identify patterns of muscle fatigue that precede muscle injuries by 3 to 7 days. A system of agents that monitors each player's physiological state and generates preventive alerts not only lowers injury risk; it lowers the risk of losing an asset worth tens of millions of euros at a critical point in the season. This is the use case where the ROI of advanced soccer analytics is most directly quantifiable.

**Tactical preparation as an asymmetric advantage.** A team that can simulate 10,000 variations of the opponent's tactics in 24 hours (based on tracking data and multi-agent models of the opposing players) arrives at every match with a level of tactical preparation that an opponent without those capabilities cannot match. Multiplied across a 38-match season, that asymmetry in preparation produces cumulative performance differences that show up in league position. In the Premier League, the difference between qualifying for the Champions League and missing out is worth an additional €50–100 million in revenue per season.

## Soccer as a Laboratory for Decision-Making Under Distributed Uncertainty

The deeper side of the connection between soccer and multi-agent systems goes beyond sports analysis: soccer is the most accessible, most observed, and best documented laboratory for studying *distributed decision-making under severe uncertainty with extreme time constraints*.

Business organizations face exactly the same problem structure: multiple actors with partial information who must coordinate to reach a collective goal, in a dynamic environment where the adversary also adapts, with decision windows too short for exhaustive analysis. Companies that study soccer as a model of distributed coordination (not as entertainment but as a formal system) get insights that carry over to organizational design, crisis management, and decision architectures.

Strategy consulting teams have started using soccer match analysis as an organizational diagnostic method: the way a team responds to losing the ball (immediate pressing versus an orderly retreat) is structurally analogous to the way an organization responds to a market crisis. The patterns are formally equivalent, and the lessons transfer.

## Key Takeaways from Chapter 28

- A soccer match meets the formal definition of a multi-agent system: 11 autonomous agents per team that perceive, reason, and coordinate under implicit protocols in real time.
- 2D and biomechanical tracking data have turned the pitch into the most data-rich multi-agent environment in the world, with 25 frames per second of complete system state.
- MARL frameworks (QMIX, MADDPG) and action valuation models (VAEP) apply directly to tactical analysis; academic research at KDD, NeurIPS, and *Nature* supports that applicability.
- Liverpool, StatsBomb, and Bayern Munich are documented cases of agentic analysis in practice: separation of responsibilities among specialized agents, orchestrated synthesis, and continuous feedback.
- The executive view: market valuation, injury risk management, and tactical preparation are the three areas where the ROI of multi-agent soccer analysis is most directly quantifiable.
- Soccer is the most accessible laboratory for studying distributed coordination under uncertainty, with direct transfer to organizational design and enterprise decision architectures.

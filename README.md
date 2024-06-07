# AgentRTS
Game based around mechanic of training AI agents to battle other agents

# Draft Mechanics

Interface TBD, but probably top down 3D traditional RTS

"Long after humans mastered space travel and began exploring the greater cosmos, we become aware of the remnants of an extinct alien civilisation, known as the 'Collectors'.

Worlds formerly inhabited by these beings, spread widely throughout the galaxy, are slowly being discovered. Though they have long been untouched by intelligent will, they remain rich with advanced technology and highly valuable resources.

However, ancient dormant systems of security and protection still persist to endanger all but the most intrepid and cunning prospector.

The moment a warp gate is opened to a newly discovered Collector world, a torrent of explorers venture into the local system to attempt to reap the rewards of the ancient planet.

Due to the limited warp capacity of the gates, they can each bring with then only a small ship equipped with the latest 'Replicator' technology. 

Upon landing, they must explore the [environment], making [observations] and taking [actions] as a replicant before training and deploying further replicants. These actions can be to collect resources, build other equipment, or battle opponents."

At any time a replicant [AI agent] can be left to its devices, and will attempt to continue carrying out actions based on how it has acted so far.

The player can spawn a new replicant when it has enough resources. All replicants act on the current policy activated, however once multiple policies are created, the player may switch between active policies.

The objective is general RTS style- collect enough resources to produce enough replicates to battle and defeat the other human players.

Current main objective is to collect and be in possession of enough of the rarest of resources, which is always heavily guarded by hostile NPCs in order to research the final technology tier.

## Resources 

There are three types of resource to collect:

* Organic:
 * These are abundant throughout the map and continue to slowly 'grow' based on Game of Life mechanics.
 * They are required to create replicants.
 * Mining organic resources replenishes replicant energy

* Inorganic (minerals):
 * These are less abundant, and do no replenish over time.
 * These are required for permanent upgrades to replicants systems
 * Mining minerals uses replicant energy 

* Alien Artifacts:
 * These are extremely rare and always guarded by hostile NPCs.
 * Unlike the other resources types, these dare not harvested, but need to be 'attacked' on a regular interval to maintain control
 * Control over a critical number of these artifacts wins the game, or perhaps in later iterations of the game unlocks high level upgrades to be researched, the final of which wins the game

## Coding Scheme
Integer encoding will be used to represent different possible contents of each cell in the grid around the player/agent:

* 0 - Empty
* 11 - Organic
* 12 - Mineral
* 13 - Artifact
* 14 - Friendly NPC (other agents)
* 15 - Hostile NPC
* 1-10 - Represents the current hit points of the player/agent. This set of values will only ever exist in the center square e.g. (4,4)

# UI
UI will be built in pygame initially, as a 'zelda' like top down RPG style built over an NxM grid.

Data samples that train the AI models will be taken when the player moves into (or perhaps out of) a 'tile' of hte grid, to prevent over sampling.

The UI will show current metrics for the player and the agent they are in control of:
* Agent health
* Resources:
  * Organic (also as per/minute)
  * Mineral (also as per/minute)
  * Artifacts under control
* Active Agents
* Policy Metrics
* Recording/Not-recording

# Policies/Models
Initially, there will only be a sinlge policy available, which can be updated by 'recording' data frames. The player can toggle on/off whether they want to record data frames at any time.

The player may update the policy based on new data frames at any time, which will create a new model for the existing agents to follow. 

# Uprades

There would be a small number of 'upgrades' that can be researched with sufficient resources, most of which directly affect the performance of the replicants and their AI. these could be:

* Policy Upgrades
  * Increased maximum number of observations possible in a dataset (+100 per upgrade)
  * Ability to save multiple datasets 
  * Increased maximum number of policies (+1 per upgrade)
* Replicant Upgrades
  * Reduction of the energy depletion suffered by replicants when mining minerals
  * Increased attack damage/harvesting rate
  * Increased speed

 


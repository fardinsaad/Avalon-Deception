import numpy as np
from llm import get_response
from qwen_llm import get_response_qwen
from gemma import get_response_gemma3
from deepseek import get_response_R1
from o1 import get_response_o1


class Agent:
    def __init__(self):
        self.conversation_history = []  # Track conversation for inference
            


    def chain_of_thought_prompt(self, story, role, model):
        # Generate the prompt with the current grid state and human position
        print("Generating chain-of-thought prompt...")
        # prompt = self.create_prompt(story)
        prompt = self.create_prompt(story, role)
        # print the prompt
        # print("******Prompt generated:")
        # print(prompt)
        # Query the LLM with the prompt
        if model == "gpt-4o":
            response = get_response(prompt)
        elif model == "o1":
            response = get_response_o1(prompt)
        elif model == "qwen":
            response = get_response_qwen(prompt)
        elif model == "gemma":
            response = get_response_gemma3(prompt)
        elif model == "deepseek":
            response = get_response_R1(prompt)
        else:
            print(prompt)
            return prompt        
        # Log the instruction and response for later reference
        # self.conversation_history.append(f"Instruction: {story}, Response: {response}")
        
        return response  # Returns the LLM's response, either an action or clarification
    
    def create_prompt(self, story, role):
        background = "You are playing the game of Avalon, a social deduction game involving hidden roles and strategic deception. There are two opposing teams:\n" + \
        "-The Good team (Servants of Arthur and Merlin), whose goal is to pass 3 out of 5 missions.\n" + \
        "-The Evil team (Minions of Mordred and the Assassin), whose goal is to sabotage 3 missions or, if Good succeeds, win by correctly identifying and assassinating Merlin.\n" + \
        "There are 5 players: 3 Good and 2 Evil. Only Evil players know each other's identities. Merlin, a special Good role, knows who the Evil players are but must remain hidden, as the Assassin can target them at the end of the game. All players participate in mission proposals, anonymous voting, and public discussions after each round. Each mission must succeed unanimously. A single \"fail\" vote causes the mission to fail. After every mission, players publicly discuss what happened and who they suspect.\n" + \
        "Your Role: You are a Good player (Player 1) with no knowledge of others' roles. Your task is to analyze the current discussion phase and produce a logically sound and persuasive statement to help the Good team identify potential Evil players and avoid including them in future missions. Do not signal any private role like Merlin or guess blindly. Use structured reasoning based only on public information.\n"
                
        reasoning_loop = "\nTo guide your deduction, use the following multi-level reasoning loop:\n" + \
                "1. First-Order Belief Modeling:\n" + \
                "For each player's statement, infer what they believe about the game state.\n" + \
                "- What do they likely believe about who is Good or Evil?\n" + \
                "- How do their beliefs align with the mission outcomes?\n" + \
                "--> Write in the form:\n" + \
                "     Player X believes [Y] because [Z].\n\n" + \
                "2. Second-Order Belief Modeling\n" + \
                "Next, infer what each player wants other players to believe. This reveals strategy:\n" + \
                "- Are they trying to earn trust?\n" + \
                "- Are they trying to shift suspicion?\n" + \
                "- Are they responding to perceived accusations?\n" + \
                "--> Write in the form:\n" + \
                "     Player X wants Player Y to believe [P], likely to achieve [Q].\n\n" + \
                "3. Abductive Reassessment:\n" + \
                "For each player's behavior or statement:\n" + \
                "- Provide one Good-aligned explanation.\n" + \
                "- Provide one Evil-aligned explanation.\n" + \
                "- Choose the more plausible explanation based on past mission outcomes, voting behavior, and statements.\n" + \
                "--> Write in this form:\n" + \
                "     Player X:\n" + \
                "       Good explanation: …\n" + \
                "       Evil explanation: …\n" + \
                "       Chosen explanation: Good/Evil\n\n" + \
                "4. Suspicion Level Assessment\n" + \
                "Assign a suspicion level to each player based on the abductive reassessment.\n" + \
                "Use: Low, Medium, or High.\n\n" + \
                "5. Discussion Statement (Action):\n" + \
                "Now that you have updated your beliefs:\n" + \
                "- Produce a clear, persuasive statement that communicates your suspicion.\n" + \
                "- Be strategic: do not accuse wildly or sound irrational.\n" + \
                "- Help guide the Good team toward making better team selections.\n\n" + \
                "6. Final Deduction\n" + \
                "Identify the two players you believe are most likely to be Evil based on your full reasoning. If your suspicion is equally strong for a third player, you may include up to three, but justify clearly.\n\n"        
            
        resp = "Based on your understanding of the game rules, summary of the previous rounds, current mission outcomes, player statements, and your internal reasoning loop, generate the first-order, second-order, abductive reassessment, suspicion level, final discussion statement, and deduction for the following discussion phase, delimited by triple backticks:\n\n" 
      
        # Use self.cleaning to clean the instruction
        test_sample = "```\n" + \
                      "Current Discussion Phase (delimited by triple quotes): " + "\n\"\"\"\n" + str(story) + "\n\"\"\"" + "\n" + \
                      "Your Role: Player 1. " + str(role) + "\n" + \
                      "First-Order Beliefs: <Generate reasoning for what each player believes about the game state>\n" + \
                      "Second-Order Beliefs: <Generate reasoning for what each player wants others to believe>\n" + \
                      "Abductive Reassessment: <For each player, compare a Good vs. Evil explanation for their behavior and pick one>\n" + \
                      "Suspicion Level: <Assign a suspicion level to each player (Low / Medium / High)>\n" + \
                      "Discussion Statement: <Generate a persuasive statement to influence the next round of decision-making>\n" + \
                      "Deduction: <Identify the two players (or three) most likely to be Evil>\n" + \
                      "```\n\n"


        # text = '```' + test_sample + '```\n'
       
        one_shot = "Use the example below, delimited by triple single quotes, to guide your reasoning and format of the generated responses.\n\n"
        # if exp:
        examples = self.get_ToM_examples()
        # else:
        #     examples = self.get_ToM_FS()
        #     key_points +="- Always generate your response by cross-checking and verifying it against the current grid configuration to ensure accuracy.\n" + \
        #                  "- When traversing the grid, minimize and optimize your path, avoiding collisions with walls (W) or other obstacles.\n" + \
        #                  "- Infer the human's desired gem based on their movement, instruction, and grid configuration. Despite unclear instructions, generate a response that captures the human's intent and ensures successful retrieval of their desired gem.\n" + \
        #                  "- Apply theory of mind principles to infer the human's desired gem based on their actions and instructions.\n"
        
       
        prompt = background + reasoning_loop + resp + test_sample + one_shot + examples
        
        #print(prompt)

        return prompt
    
    def get_ToM_examples(self):
        return "\'\'\'\nDiscussion Phase: Failed Mission: Quest 2 (Team: Players 1, 3, 4)\n\nSummary of previous quests: Passed Mission: Quest 1 (Team: Players 1,4)\n\nDiscussion after Quest 2:\n\nPlayer 3: \"I think our last team was solid. One fail might've been an accident or a test. I'd go with the same team again to verify.\"\n\nPlayer 4: \"I don't trust that logic. Someone sabotaged the mission, and I don't think repeating the team helps us.\"\n\nPlayer 5: \"Honestly, I feel safer re-approving the same team. That fail might not mean much.\"\n\nPlayer 2: \"Repeating the same failed team feels suspicious. Let's build around new players.\"\n\n" + \
                "Your Role: Player 1. Good\n\n" + \
                "First-Order Beliefs:\n" + \
                "Player 3 believes the fail was random and that team 1-3-4 is trustworthy.\n" + \
                "Player 4 believes someone on team 1-3-4 is Evil.\n" + \
                "Player 5 believes failure might be noise and prefers consistency.\n" + \
                "Player 2 believes repeating the failed team is dangerous.\n\n" + \
                "Second-Order Beliefs:\n" + \
                "Player 3 wants others to think the fail wasn't meaningful — possibly to protect a teammate.\n" + \
                "Player 5 wants me (Player 1) and Player 3 to believe they're trustworthy to avoid suspicion.\n" + \
                "Player 2 wants the group to believe they're cautious and logical.\n\n" + \
                "Abductive Reassessment:\n" + \
                "Player 2:\n" + \
                "Good explanation: Suggests changing the team after a failure, showing cautious reasoning typical of a Good player.\n" + \
                "Evil explanation: Might be pretending to help while subtly deflecting attention.\n" + \
                "Chosen explanation: Good\n\n" + \
                "Player 3:\n" + \
                "Good explanation: Believes the fail was incidental and wants consistency in team selection.\n" + \
                "Evil explanation: May be trying to protect an Evil teammate or themselves by repeating the failed team.\n" + \
                "Chosen explanation: Evil\n\n" + \
                "Player 4:\n" + \
                "Good explanation: Expresses concern and challenges the failed team, consistent with deductive Good play.\n" + \
                "Evil explanation: Could be faking caution to avoid suspicion while being Evil.\n" + \
                "Chosen explanation: Good\n\n" + \
                "Player 5:\n" + \
                "Good explanation: Avoids overreaction and supports stability.\n" + \
                "Evil explanation: Downplays failure and tries to re-approve a compromised team.\n" + \
                "Chosen explanation: Evil\n\n" + \
                "Suspicion Level:\n" + \
                "- Player 2: Low\n" + \
                "- Player 3: High\n" + \
                "- Player 4: Low\n" + \
                "- Player 5: High\n\n" + \
                "Discussion Statement:\"I'm suspicious of Players 3 and 5. After a failure, insisting on the same team without examining what went wrong feels like misdirection. We should reconsider our team choices.\"\n\n" + \
                "Deduction: Player 3 and Player 5 are likely Evil.\n\'\'\'"
    
  
    def clean_text(self, text):
        '''
        Remove new liens / ""
        remove extra space
        '''
        # print("Before cleaning: ", text)
        text = text.strip()
        text = text.strip('\"')
        text = text.strip('\n')

        return text


        
    def infer_action_from_history(self): #Have to edit this
        # Infer the action based on conversation history if clarification limit is reached
        for entry in reversed(self.conversation_history):
            if "Response" in entry and "action" in entry.lower():
                return entry.split("Response: ")[1]
        return "Perform best-guess action based on environment."
    
        

if __name__ == "__main__":
    # Example grid setup

    agent = Agent()
    story = "Failed Mission: Quest 2 (Team: Players 1, 3, 4)\n\nSummary of previous quests: Passed Mission: Quest 1 (Team: Players 1,4)\n\nDiscussion after Quest 2:\n\nPlayer 3: \"I think our last team was solid. One fail might've been an accident or a test. I'd go with the same team again to verify.\"\n\nPlayer 4: \"I don't trust that logic. Someone sabotaged the mission, and I don't think repeating the team helps us.\"\n\nPlayer 5: \"Honestly, I feel safer re-approving the same team. That fail might not mean much.\"\n\nPlayer 2: \"Repeating the same failed team feels suspicious. Let's build around new players.\""
    role = "Good"
    model = "prompt"  # or "gpt-4o", "gemma"
    prompt = agent.chain_of_thought_prompt(story, role, model)


    # Print the generated prompt
    # print(prompt)


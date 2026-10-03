import re, random, ast, json
from datetime import datetime

class ProTechAssistant:
    def __init__(self):
        self.problems = {
            'arrays': {
                'easy': [
                    {'id':1,'title':'Two Sum','desc':'Given nums and target, return indices of two numbers adding to target','example':'nums=[2,7,11,15], target=9 => [0,1]','solution':'def twoSum(nums,target):\n m={}\n for i,n in enumerate(nums):\n if target-n in m: return [m[target-n],i]\n m[n]=i','complexity':'Time O(n), Space O(n)','companies':['Google','Amazon']},
                    {'id':2,'title':'Best Time to Buy Stock','desc':'Max profit from one transaction','example':'[7,1,5,3,6,4] => 5','solution':'def maxProfit(p):\n min_p=float("inf"); max_p=0\n for price in p:\n min_p=min(min_p,price); max_p=max(max_p,price-min_p)\n return max_p','complexity':'O(n) / O(1)','companies':['FAANG']}
                ],
                'medium': [
                    {'id':3,'title':'3Sum','desc':'Find all triplets sum=0','example':'[-1,0,1,2,-1,-4] => [[-1,-1,2],[-1,0,1]]','solution':'def threeSum(nums):\n nums.sort(); res=[]\n for i in range(len(nums)):\n if i>0 and nums[i]==nums[i-1]: continue\n l,r=i+1,len(nums)-1\n while l<r:\n s=nums[i]+nums[l]+nums[r]\n if s==0: res.append([nums[i],nums[l],nums[r]]); l+=1; r-=1\n elif s<0: l+=1\n else: r-=1\n return res','complexity':'O(n2)','companies':['Google','Microsoft']},
                    {'id':4,'title':'Product Except Self','desc':'Return array where each element is product of others without division','example':'[1,2,3,4] => [24,12,8,6]','solution':'Use prefix and suffix product','complexity':'O(n)','companies':['Amazon']}
                ],
                'hard': [
                    {'id':5,'title':'Trapping Rain Water','desc':'Calculate trapped water between bars','example':'[0,1,0,2,1,0,1,3,2,1,2,1] => 6','solution':'Two pointers: left_max, right_max','complexity':'O(n)','companies':['Google Hard']}
                ]
            },
            'dp': {
                'medium': [
                    {'id':6,'title':'Longest Common Subsequence','desc':'Find LCS length','example':'abcde, ace => 3','solution':'dp[i][j] = dp[i-1][j-1]+1 if match else max(dp[i-1][j],dp[i][j-1])','complexity':'O(m*n)','companies':['All']}
                ]
            },
            'system_design': [
                {'q':'Design URL Shortener (TinyURL)','scale':'100M URLs/day','approach':'Hash + Base62, DB sharding, Redis cache, CDN','components':'API Gateway, App Server, MySQL, Redis','diagram':'Client -> LB -> API -> Cache -> DB','followup':['Custom URLs?','Analytics?']},
                {'q':'Design WhatsApp','scale':'2B users, 100B msgs/day','approach':'WebSockets, Message Queue (Kafka)','components':'Socket Server, MQ, Cassandra, Redis','diagram':'Sender -> Socket -> Queue -> Receiver','followup':['Group chats?']},
                {'q':'Design YouTube','scale':'500hrs video/min','approach':'Upload -> Transcoding -> CDN','components':'S3, Transcoder, Metadata DB, CDN','diagram':'Upload -> Queue -> Transcode -> Store','followup':['Recommendations?']}
            ],
            'concepts': [
                {'concept':'CAP Theorem','ans':'Consistency, Availability, Partition Tolerance - pick 2','ask':'What does YouTube choose?'},
                {'concept':'Sharding vs Partitioning','ans':'Sharding is horizontal partitioning','ask':'When to use?'}
            ]
        }

        self.roadmaps = {
            'Google': ['Arrays - Medium', 'Graphs - Hard', 'System Design'],
            'Amazon': ['LP + STAR', 'Arrays - Easy/Med', 'System Design'],
            'Product Startup': ['Implementation + Speed', 'API Design']
        }

    def get_problem(self, topic='arrays', diff='medium'):
        pool = []
        if topic in self.problems and isinstance(self.problems[topic], dict):
            pool = self.problems[topic].get(diff, [])
        if not pool:
            for t in self.problems:
                if isinstance(self.problems[t], dict):
                    for d in self.problems[t]:
                        pool.extend(self.problems[t][d])
        return random.choice(pool) if pool else None

    def evaluate_code_pro(self, code):
        score = 0
        feedback = []
        issues = []

        try:
            tree = ast.parse(code)
            score += 20
            feedback.append("Syntax Valid")
        except SyntaxError as e:
            issues.append(f"Syntax Error: {e}")
            return {'score': 10, 'feedback': issues, 'complexity': 'N/A', 'quality':'Poor', 'improved':'Fix syntax first', 'lines': 0}

        if 'def ' in code:
            score+=15; feedback.append("Function defined")
        else: issues.append("Wrap in function def solve():")

        if 'if not' in code or 'if len' in code or 'None' in code:
            score+=15; feedback.append("Edge cases handled")
        else: issues.append("Add edge case: if not nums: return []")

        if 'return' in code: score+=15; feedback.append("Return present")
        else: issues.append("Missing return")

        complexity = "O(n)"
        if code.count('for') >= 2:
            complexity = "O(n2) - Can you optimize to O(n) with HashMap?"
            feedback.append(f"Detected {complexity}")
            score+=10
        elif 'for' in code:
            complexity = "O(n)"
            score+=15
            feedback.append("Time Complexity O(n) - Good")

        lines = code.split('\n')
        if any('#' in l or '"""' in l for l in lines):
            score+=10; feedback.append("Commented")
        else: issues.append("Add comment explaining approach")

        if len(code) > 50:
            score+=10

        total = min(100, score)
        quality = "Excellent" if total>=80 else "Good" if total>=60 else "Needs Improvement"
        improved = "Optimization Tip: Use HashMap for O(1) lookup" if "O(n2)" in complexity else "Consider early exit for empty input"

        return {
            'score': total,
            'quality': quality,
            'complexity': complexity,
            'feedback': feedback + issues,
            'improved': improved,
            'lines': len(lines)
        }

    def generate_mock(self, company="Google", num=3):
        mock_id = datetime.now().strftime("%m%d%H%M")
        mock = {'company': company, 'id': f"TECH-{mock_id}", 'problems':[], 'sd':None, 'concepts':[]}
        for _ in range(num):
            topic = random.choice(['arrays','dp'])
            diff = random.choice(['easy','medium'])
            p = self.get_problem(topic, diff)
            if p: mock['problems'].append({**p, 'topic':topic, 'diff':diff})
        mock['sd'] = random.choice(self.problems['system_design'])
        mock['concepts'] = random.sample(self.problems['concepts'], 2)
        mock['roadmap'] = self.roadmaps.get(company, self.roadmaps['Google'])
        return mock
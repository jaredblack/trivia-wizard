export class AnswerObject {
    teamName: string;
    answer: string;
    questionIndex: string;
    teamScore: number;
    pointsGiven: number;

    constructor(teamName: string, answer: string, questionIndex: string, teamScore: number, pointsGiven: number) {
        this.teamName = teamName;
        this.answer = answer;
        this.questionIndex = questionIndex;
        this.teamScore = teamScore;
        this.pointsGiven = pointsGiven;
    }
}

export class TeamScore {
    teamName: string;
    score: number;

    constructor(teamName: string, score: number) {
        this.teamName = teamName;
        this.score = score;
    }
}

export class BonusIndices {
    indices: number[] = [];
    numBonusesAvailable: number;

    constructor(numBonusesAvailable: number) {
        this.numBonusesAvailable = numBonusesAvailable;
    }

    /**
     * Adds an index to the bonus indices if it is less than the current bonus indices, or if there is an empty spot.
     * @param index
     * @returns true if the index was added, false otherwise
     */
    public addBonusIndex(index: number): boolean {
        this.indices.push(index);
        this.indices.sort((a, b) => a - b);
        if (this.indices.length > this.numBonusesAvailable) {
            this.indices.pop();
        }
        return this.indices.includes(index);
    }

    /**
     * Gets the weight of a bonus index. For example, if this returns 2, then the bonus is worth 2 * (bonus amount)
     * @param index 
     * @returns the weight of the bonus index
     */
    public getBonusWeight(index: number): number {
        const indexOfIndex = this.indices.indexOf(index);
        if (indexOfIndex === -1) {
            return 0;
        }
        return this.indices.length - indexOfIndex;
    }
}
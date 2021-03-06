import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probability = 1

    for person in people:
        # Get mother, father, number of gene and trait of each person 
        gene_number = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False

        mother = people[person]['mother']
        father = people[person]['father']

        # If person has no info about parent
        if mother == None and father == None:
            joint_probability = PROBS['gene'][gene_number] * PROBS['trait'][gene_number][trait] 
        
        # If info about parent is available
        else:
            probability = {}

            for parent in [mother, father]:
                parent_gene_number = 1 if parent in one_gene else 2 if parent in two_genes else 0
                
                # chance that a person in set 'no_gene' stay harmless to its child
                if parent_gene_number == 0:
                    probability[parent] = PROBS['mutation']

                elif parent_gene_number == 1:
                    probability[parent] = 0.5 * (1 - PROBS['mutation']) + 0.5 * PROBS['mutation']
               
                # chance that a person in set 'two_gene' stay harmful to its child
                else:
                    probability[parent] = 1 - PROBS['mutation']
            
            # if none of parent has a copy of gene
            # chance that they are passing a harmless gene to their child is
            if gene_number == 0:
                joint_probability = probability[mother] * probability[father]
            
            # if one person has a copy of gene
            elif gene_number == 1:
                joint_probability = (1 - probability[mother]) * probability[father] + probability[mother] * (1 - probability[father])

            # if both people have a copy of gene
            else:
                joint_probability = (1 - probability[mother]) * (1 - probability[father])

            # Chance that a person stay correct to its assigned group
            trait_probability = PROBS['trait'][gene_number][trait]
            joint_probability *= trait_probability

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Update the gene distribution
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
    
        # Update the trait distribution
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize a person's trait
        total_trait = 0
        for i in [True, False]:
            total_trait += probabilities[person]["trait"][i] 

        for i in [True, False]:    
            probabilities[person]["trait"][i] /= total_trait

        # Normalize a person's gene
        total_gene = 0
        for i in range (0,3):
            total_gene += probabilities[person]["gene"][i]

        for i in range (0,3):
            probabilities[person]["gene"][i] /= total_gene

if __name__ == "__main__":
    main()

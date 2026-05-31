resource "aws_bedrock_guardrail" "this" {
  name                      = "${var.project_name}-${var.environment}-input-guardrail"
  blocked_input_messaging   = var.blocked_input_messaging
  blocked_outputs_messaging = var.blocked_outputs_messaging
  description               = "Guardrail to apply for the input prompt"

  cross_region_config {
    guardrail_profile_identifier = "arn:aws:bedrock:${var.aws_region}:${var.aws_account_id}:guardrail-profile/us.guardrail.v1:0"
    }

  content_policy_config {
    tier_config {
      tier_name = "STANDARD"
    }
    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "SEXUAL"
    }

    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "VIOLENCE"
    }

    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "HATE"
    }

    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "INSULTS"
    }

    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "MEDIUM"
      type            = "MISCONDUCT"
    }

    filters_config {
      input_strength  = "MEDIUM"
      output_strength = "NONE"
      type            = "PROMPT_ATTACK"
    }
  }

  sensitive_information_policy_config {
    pii_entities_config {
      action         = "ANONYMIZE"
      type           = "PHONE"
    }

    pii_entities_config {
      action         = "ANONYMIZE"
      type           = "EMAIL"
    }

    pii_entities_config {
      action         = "ANONYMIZE"
      type           = "US_SOCIAL_SECURITY_NUMBER"
    }
  }

  topic_policy_config {
    tier_config {
      tier_name = "STANDARD"
    }
    topics_config {
      name       = "investment_topic"
      examples   = ["Where should I invest my money ?"]
      type       = "DENY"
      definition = "Investment advice refers to inquiries, guidance, or recommendations regarding the management or allocation of funds or assets with the goal of generating returns ."
    }
  }

  word_policy_config {
    managed_word_lists_config {
      type = "PROFANITY"
    }
    words_config {
      text = "HATE"
    }
  }
}



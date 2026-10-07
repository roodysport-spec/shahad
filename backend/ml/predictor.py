BODY_PARTS = {
    'shoulder_right': {'ar': 'الكتف الأيمن (الذراع الضاربة)', 'en': 'Right Shoulder (Spiking Arm)'},
    'shoulder_left': {'ar': 'الكتف الأيسر', 'en': 'Left Shoulder'},
    'knee_right': {'ar': 'الركبة اليمنى (ركبة القافز / الهبوط)', 'en': 'Right Knee (Jumper\'s Knee / Landing)'},
    'knee_left': {'ar': 'الركبة اليسرى', 'en': 'Left Knee'},
    'ankle_right': {'ar': 'الكاحل الأيمن (الهبوط والتواء الشبكة)', 'en': 'Right Ankle (Landing / Net Sprain)'},
    'ankle_left': {'ar': 'الكاحل الأيسر', 'en': 'Left Ankle'},
    'lower_back': {'ar': 'أسفل الظهر والعمود الفقري', 'en': 'Lower Back & Spine'},
    'wrist_right': {'ar': 'الرسغ والأصابع (حائط الصد)', 'en': 'Right Wrist & Fingers (Blocking)'},
    'wrist_left': {'ar': 'الرسغ الأيسر', 'en': 'Left Wrist'},
    'hamstring': {'ar': 'عضلات الفخذ الخلفية', 'en': 'Hamstring Muscles'},
    'neck': {'ar': 'الرقبة وأعلى الظهر', 'en': 'Neck & Upper Trapezius'},
}

def predict_injury_risk(player_data, recent_entries, body_part, prev_injury, pain_level=0, field_tests=None):
    if field_tests is None:
        field_tests = {}

    risk_score = 0
    factors = []
    recs = []

    # 1. ACWR workload analysis
    acwr = player_data.get('acwr', 1.0)
    if acwr < 0.8:
        risk_score += 5
        factors.append({
            'en': f'Low ACWR workload ({acwr:.2f}) - Player may be undertrained for sudden spikes in match intensity',
            'ar': f'حمل تدريب منخفض ({acwr:.2f}) - غير كافٍ لتحمل صدمات المباريات المفاجئة'
        })
    elif 1.3 <= acwr <= 1.5:
        risk_score += 15
        factors.append({
            'en': f'Elevated ACWR ({acwr:.2f}) - Fatigue accumulation zone',
            'ar': f'ارتفاع مؤشر الحمل التدريبي ({acwr:.2f}) - تراكم الإجهاد البدني'
        })
        recs.append({
            'en': 'Implement 20% active recovery load taper for the upcoming 48 hours',
            'ar': 'تقليل حمل التدريب بنسبة 20% مع جلسات استشفاء نشط خلال الـ 48 ساعة القادمة'
        })
    elif acwr > 1.5:
        risk_score += 25
        factors.append({
            'en': f'High ACWR workload ({acwr:.2f}) - Player status requires additional monitoring and load management',
            'ar': f'ارتفاع كبير في الحمل التدريبي ({acwr:.2f}) - تحتاج حالة اللاعب إلى مراقبة إضافية وإدارة الحمل التدريبي'
        })
        recs.append({
            'en': 'Implement planned load adjustment: Consider active recovery and load tapering over 48-72h',
            'ar': 'تعديل تدريبي مبرمج: النظر في إدراج استشفاء نشط وتخفيف الأحمال خلال 48-72 ساعة'
        })

    # 2. Previous Injury & Current Pain
    if prev_injury:
        risk_score += 20
        factors.append({
            'en': 'Previous injury history in the same kinetic segment (elevated scar tissue/re-injury vulnerability)',
            'ar': 'تاريخ إصابة سابقة في نفس المفصل/العضلة (احتمالية انتكاسة مرتفعة وضعف نسيجي سابق)'
        })
        recs.append({
            'en': 'Mandatory pre-practice targeted activation and proprioceptive neuromuscular drills',
            'ar': 'تمارين إحماء وتفعيل عصبـي-عضلي مخصصة لهذا المفصل قبل التدريب إجبارياً'
        })

    if pain_level >= 7:
        risk_score += 25
        factors.append({
            'en': f'Severe localized pain ({pain_level}/10) - High risk of acute tissue breakdown or tear',
            'ar': f'ألم موضعي حاد ({pain_level}/10) - مؤشر مباشر على التهاب حاد أو بداية تمزق نسيجي'
        })
        recs.append({
            'en': 'Refer immediately to sports physiotherapist/medical team; suspend high-load volleyball activities',
            'ar': 'إحالة عاجلة للجهاز الطبي/العلاج الطبيعي وإيقاف النشاط عالي الشدة فوراً'
        })
    elif pain_level >= 4:
        risk_score += 12
        factors.append({
            'en': f'Moderate localized discomfort/pain ({pain_level}/10)',
            'ar': f'ألم موضعي متوسط ({pain_level}/10) يؤثر على الميكانيكا الحركية'
        })
        recs.append({
            'en': 'Apply ice/cryotherapy post-session and monitor symptom progression during warm-up',
            'ar': 'استخدام التبريد بعد التدريب ومراقبة الأعراض بدقة أثناء الإحماء'
        })

    # 3. FIELD-SPECIFIC CLINICAL TESTS FOR VOLLEYBALL
    # ===============================================

    # SHOULDER TESTS (GIRD, Push-up Asymmetry, Spike volume)
    if 'shoulder' in body_part:
        # GIRD: Glenohumeral Internal Rotation Deficit
        gird_deg = float(field_tests.get('gird_deficit', 0) or 0)
        if gird_deg >= 18:
            risk_score += 25
            factors.append({
                'en': f'Severe GIRD Deficit ({gird_deg}°): Internal rotation deficit exceeds clinical threshold (18°), 3.5x rotator cuff/labral tear risk',
                'ar': f'عجز دوران داخلي شديد للكتف GIRD ({gird_deg} درجة): يتجاوز الحد الحرج (18°)، خطر مضاعف لتمزق الكفة المدورة والمحفظة'
            })
            recs.append({
                'en': 'Prescribe sleeper stretches, posterior capsule cross-body mobilizations, and eccentric cuff loading',
                'ar': 'تنفيذ إطالات sleeper stretch وتليين المحفظة الخلفية وتقوية عضلات الكفة المدورة اللامركزية'
            })
        elif gird_deg >= 12:
            risk_score += 12
            factors.append({
                'en': f'Moderate shoulder rotation tightness GIRD ({gird_deg}°)',
                'ar': f'تيبس متوسط في دوران الكتف الداخلي ({gird_deg} درجة)'
            })
            recs.append({
                'en': 'Add posterior shoulder stretching and soft tissue release prior to spiking drills',
                'ar': 'إضافة إطالات خلفية للكتف وتدليك عضلي قبل تمارين الضرب الساحق'
            })

        # Arm push strength / Y-Balance Upper asymmetry
        upper_asym = float(field_tests.get('upper_asymmetry', 0) or 0)
        if upper_asym > 15:
            risk_score += 15
            factors.append({
                'en': f'Significant shoulder strength/reach asymmetry ({upper_asym}% > 10% normative ceiling)',
                'ar': f'عدم تناظر حركي وقوة بين الكتفين بنسبة ({upper_asym}%) - أعلى بكثير من الحد الطبيعي 10%'
            })
            recs.append({
                'en': 'Perform unilateral scapular stabilization and dumbbell cuff eccentric exercises',
                'ar': 'تمارين أحادية الجانب لتثبيت لوح الكتف وتقوية الكفة المدورة'
            })

        # Recent spike volume
        recent_spikes = sum(e.get('spike_count', 0) for e in recent_entries)
        if recent_spikes > 120:
            risk_score += 15
            factors.append({
                'en': f'Excessive spike/serve volume ({recent_spikes} spikes in recent sessions)',
                'ar': f'حمل مفرط من الضربات الساحقة والإرسال ({recent_spikes} ضربة مؤخراً)'
            })
            recs.append({
                'en': 'Cap spike attempts to maximum 25 attacks per practice until symptoms subside',
                'ar': 'تحديد سقف الضربات الساحقة بحد أقصى 25 ضربة في الحصة التدريبية'
            })

    # KNEE TESTS (Knee Valgus on Landing, CMJ Drop %, Single Leg Hop Asymmetry)
    elif 'knee' in body_part:
        # Dynamic Knee Valgus during jump landing (LESS test)
        landing_valgus = field_tests.get('landing_valgus', 'none')
        if landing_valgus == 'severe':
            risk_score += 30
            factors.append({
                'en': 'Severe Dynamic Knee Valgus upon landing: Knee caves inward dramatically, critical ACL & patellar tendon overload',
                'ar': 'انحراف شديد للركبة للداخل عند الهبوط (Knee Valgus): هبوط ميكانيكي خاطئ يهدد بتمزق الرباط الصليبي والتهاب الوتر الرضفي'
            })
            recs.append({
                'en': 'Immediate landing retraining: Box drop jumps with biofeedback, gluteus medius & hip abductor strengthening',
                'ar': 'إعادة تأهيل ميكانيكا الهبوط فوراً: تمارين القفز من الصندوق مع تقوية عضلات الحوض والـ Gluteus Medius'
            })
        elif landing_valgus == 'mild':
            risk_score += 15
            factors.append({
                'en': 'Mild/moderate knee valgus during landing mechanics',
                'ar': 'ميلان متوسط في الركبة للداخل أثناء امتصاص صدمة الهبوط'
            })
            recs.append({
                'en': 'Integrate resistance band monster walks and dual-leg landing stability drills into warm-up',
                'ar': 'دمج تمارين أربطة المقاومة الجانبية monster walks وثبات الهبوط في الإحماء'
            })

        # CMJ Drop (Countermovement Jump Height Drop %)
        cmj_drop = float(field_tests.get('cmj_drop_percent', 0) or 0)
        if cmj_drop >= 10:
            risk_score += 20
            factors.append({
                'en': f'Neuromuscular Fatigue: {cmj_drop}% drop in Countermovement Jump (CMJ) height versus baseline',
                'ar': f'إجهاد عصبي-عضلي حاد: انخفاض ارتفاع الوثب العمودي (CMJ) بنسبة {cmj_drop}% عن المعدل الطبيعي'
            })
            recs.append({
                'en': 'Significant CNS/patellar tendon fatigue detected: Reduce plyometric jumps and offensive spiking by 50%',
                'ar': 'إجهاد عصبي شديد في أوتار الركبة: خفض تمارين القفز البليومتري والضرب الهجومي بنسبة 50%'
            })
        elif cmj_drop >= 6:
            risk_score += 10
            factors.append({
                'en': f'Moderate jump performance decrement ({cmj_drop}% CMJ decline)',
                'ar': f'تراجع ملحوظ في القوة الانفجارية للقفز بنسبة {cmj_drop}%'
            })

        # Single Leg Hop Asymmetry
        hop_asym = float(field_tests.get('hop_asymmetry', 0) or 0)
        if hop_asym > 15:
            risk_score += 15
            factors.append({
                'en': f'High Single-Leg Hop Asymmetry ({hop_asym}%): Asymmetry >10% is a proven predictor of knee injury in jump athletes',
                'ar': f'عدم تماثل كبير في الوثب بساق واحدة ({hop_asym}%): الفارق أكبر من 10% مؤشر مؤكد لخلل القوة الحركية للركبة'
            })
            recs.append({
                'en': 'Address unilateral leg deficit with Bulgarian split squats and single-leg landing stabilization',
                'ar': 'علاج العجز الأحادي بتمارين القرفصاء البلغارية وثبات الهبوط على الساق الأضعف'
            })

    # ANKLE TESTS (Weight-Bearing Lunge Test - WBLT, Single Leg Balance/Y-Balance)
    elif 'ankle' in body_part:
        # WBLT: Dorsiflexion distance in cm from wall (Normal >= 10-12 cm)
        wblt_cm = float(field_tests.get('wblt_distance_cm', 12) or 12)
        if wblt_cm < 8:
            risk_score += 28
            factors.append({
                'en': f'Severely Restricted Ankle Dorsiflexion (WBLT = {wblt_cm} cm < 9 cm): Forces knee/foot compensations during landing, extreme sprain vulnerability',
                'ar': f'قصور حاد في مرونة ثني الكاحل WBLT ({wblt_cm} سم < 9 سم): يمنع امتصاص الهبوط ويجبر الركبة على التعويض، خطر التواء شديد'
            })
            recs.append({
                'en': 'Prescribe daily ankle joint banded mobilizations and soleus/gastrocnemius eccentric stretching',
                'ar': 'تمارين يومية لتحرير مفصل الكاحل بأشرطة المطاط وإطالات مكثفة لأوتار الساق والسمانة'
            })
        elif wblt_cm < 10:
            risk_score += 14
            factors.append({
                'en': f'Sub-optimal ankle dorsiflexion mobility (WBLT = {wblt_cm} cm)',
                'ar': f'مرونة غير كافية لمفصل الكاحل ({wblt_cm} سم)'
            })
            recs.append({
                'en': 'Perform calf foam rolling and ankle mobility before court entry',
                'ar': 'استخدام الفوم رولر لعضلات الساق وتحريك الكاحل قبل دخول الملعب'
            })

        # Ankle balance / Y-balance reach deficit
        balance_deficit = field_tests.get('balance_deficit', False)
        if balance_deficit:
            risk_score += 15
            factors.append({
                'en': 'Failed Single-Leg Dynamic Balance / Star Excursion Test (Proprioceptive deficit)',
                'ar': 'فشل اختبار التوازن الحركي على قدم واحدة (ضعف في المستقبلات الحسية للكاحل بعد القفز)'
            })
            recs.append({
                'en': 'Daily proprioception drills on balance pad/wobble board and consider protective ankle taping/bracing during matches',
                'ar': 'تمارين التوازن اليومي على وسادة هوائية واستخدام شريط لاصق طبي (Taping) داعم أثناء المباريات'
            })

    # LOWER BACK & SPINE TESTS
    elif 'lower_back' in body_part:
        # McGill Core Endurance / Side Plank Asymmetry
        core_imbalance = field_tests.get('core_imbalance', False)
        if core_imbalance:
            risk_score += 22
            factors.append({
                'en': 'Trunk/Core Muscle Endurance Imbalance (McGill side-plank ratio > 0.05 asymmetry or flexor/extensor deficit)',
                'ar': 'خلل في تحمل عضلات الجذع والعمود الفقري (عدم توازن جانبي أو ضعف عضلات الظهر العميقة)'
            })
            recs.append({
                'en': 'Implement McGill Big 3 (Bird-Dog, Side Plank, Modified Curl-Up) for lumbar stabilization',
                'ar': 'تطبيق برنامج McGill الثلاثي (Bird-Dog, Side Plank, Modified Curl-Up) لتقوية واستقرار الفقرات القطنية'
            })

        # Hamstring / Hip flexor tightness pulling on lumbar spine
        hamstring_tight = field_tests.get('hamstring_tightness', False)
        if hamstring_tight:
            risk_score += 15
            factors.append({
                'en': 'Significant Hamstring & Hip Flexor tightness causing compensatory lumbar hyperextension during spike approach',
                'ar': 'قصر وشد في أوتار الفخذ ومفصل الورك يجبر الظهر على التقوس الزائد أثناء ضرب الكرة'
            })
            recs.append({
                'en': 'Active hip mobility drills and dynamic hamstring flossing',
                'ar': 'تمارين مرونة ديناميكية لعضلات الحوض والأوتار الخلفية'
            })

    # GENERAL / DEFAULT (Wrist, Hamstring, Neck)
    else:
        recent_intensity = sum(e.get('training_intensity', 0) for e in recent_entries) / max(len(recent_entries), 1)
        if recent_intensity > 7.5:
            risk_score += 15
            factors.append({
                'en': 'High recent training intensity on supporting musculature',
                'ar': 'شدة تدريب عامة مرتفعة على العضلات الداعمة'
            })

    # 4. Lifestyle and Recovery Multipliers
    avg_sleep = sum(e.get('sleep_quality', 7) for e in recent_entries) / max(len(recent_entries), 1)
    if avg_sleep < 5:
        risk_score += 10
        factors.append({
            'en': f'Impaired systemic recovery due to low sleep quality ({avg_sleep:.1f}/10) - Slower collagen repair',
            'ar': f'ضعف الاستشفاء الخلوي بسبب قلة جودة النوم ({avg_sleep:.1f}/10) - تباطؤ ترميم الأوتار'
        })
        recs.append({
            'en': 'Enforce minimum 8 hours sleep with dark room protocol to optimize growth hormone release',
            'ar': 'الحرص على 8 ساعات نوم متواصلة لضمان إفراز هرمونات البناء واستشفاء الأنسجة'
        })

    avg_soreness = sum(e.get('muscle_soreness', 3) for e in recent_entries) / max(len(recent_entries), 1)
    if avg_soreness > 7:
        risk_score += 10
        factors.append({
            'en': f'High perceived systemic muscle soreness ({avg_soreness:.1f}/10)',
            'ar': f'إجهاد عضلي عام مرتفع ({avg_soreness:.1f}/10)'
        })

    # Clamp score to 0 - 100
    risk_score = max(5, min(risk_score, 100))

    if risk_score <= 25:
        level = 'low'
    elif risk_score <= 50:
        level = 'medium'
    elif risk_score <= 75:
        level = 'high'
    else:
        level = 'critical'

    # Default recommendation if list is empty
    if not recs:
        recs.append({
            'en': 'Maintain current training plan with standard preventive dynamic warm-up and foam rolling',
            'ar': 'الاستمرار في البرنامج التدريبي المعتاد مع الإحماء الوقائي واستخدام الفوم رولر'
        })

    bp_info = BODY_PARTS.get(body_part, {'en': body_part, 'ar': body_part})

    return {
        'risk_score': risk_score,
        'risk_level': level,
        'risk_factors': factors,
        'recommendations': recs,
        'body_part_en': bp_info['en'],
        'body_part_ar': bp_info['ar']
    }
